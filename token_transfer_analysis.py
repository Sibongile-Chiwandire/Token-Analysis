# Token Transfer Analysis - Complete Python Script

import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Constants
BASE_URL = "https://xcap-mainnet.explorer.xcap.network/api/v2/token-transfers"

def fetch_all_pages():
    all_data = []
    page = 1
    while True:
        url = f"{BASE_URL}?page={page}&limit=100"
        response = requests.get(url)
        if response.status_code != 200:
            break
        data = response.json()
        if not data:
            break
        all_data.extend(data)
        page += 1
    return all_data

def clean_and_transform(data):
    df = pd.json_normalize(data)
    df['token.decimals'] = pd.to_numeric(df['token.decimals'], errors='coerce')
    df['total.value'] = pd.to_numeric(df['total.value'], errors='coerce')
    df['value'] = df['total.value'] / (10 ** df['token.decimals'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df.drop_duplicates(inplace=True)
    df.dropna(subset=['timestamp', 'value'], inplace=True)
    df['token.exchange_rate'] = pd.to_numeric(df['token.exchange_rate'], errors='coerce')
    df['usd_volume'] = df['value'] * df['token.exchange_rate']
    df['date'] = df['timestamp'].dt.date
    return df

def save_charts(df):
    sns.set(style="whitegrid")

    # Daily transaction volume
    daily_volume = df.groupby(['token.symbol', 'date'])['value'].sum().unstack(0).fillna(0)
    daily_volume.plot(figsize=(12, 6), title="Daily Token Transaction Volume")
    plt.ylabel("Volume")
    plt.xlabel("Date")
    plt.tight_layout()
    plt.savefig("daily_volume_chart.png")
    plt.close()

    # Minting and burning over time
    mint_df = df[df['type'] == 'token_minting'].groupby('date')['value'].sum()
    burn_df = df[df['type'] == 'token_burning'].groupby('date')['value'].sum()
    mint_df.plot(label='Minted', color='blue', figsize=(12, 6))
    burn_df.plot(label='Burned', color='red')
    plt.legend()
    plt.title('Daily Token Minting and Burning')
    plt.ylabel('Token Amount')
    plt.xlabel('Date')
    plt.tight_layout()
    plt.savefig("mint_burn_chart.png")
    plt.close()

    # Total supply over time
    mint_burn = df.pivot_table(index='date', columns='type', values='value', aggfunc='sum').fillna(0)
    mint_burn['total_supply'] = mint_burn.get('token_minting', 0).cumsum() - mint_burn.get('token_burning', 0).cumsum()
    mint_burn['total_supply'].plot(figsize=(12, 6), title="Total Supply of Tokens Over Time")
    plt.ylabel("Token Supply")
    plt.xlabel("Date")
    plt.tight_layout()
    plt.savefig("supply_over_time_chart.png")
    plt.close()

    # Top 10 holders (minted - burned + received - sent)
    received = df.groupby('to.hash')['value'].sum()
    sent = df.groupby('from.hash')['value'].sum()
    minted = df[df['type'] == 'token_minting'].groupby('to.hash')['value'].sum()
    burned = df[df['type'] == 'token_burning'].groupby('from.hash')['value'].sum()

    address_df = pd.DataFrame({'received': received, 'sent': sent}).fillna(0)
    address_df['minted'] = minted
    address_df['burned'] = burned
    address_df.fillna(0, inplace=True)
    address_df['net'] = address_df['minted'] - address_df['burned'] + address_df['received'] - address_df['sent']
    address_df['net'].sort_values(ascending=False).head(10).plot(kind='bar', title='Top 10 Token Holders', figsize=(10, 6))
    plt.ylabel("Net Tokens Held")
    plt.tight_layout()
    plt.savefig("top_holders_chart.png")
    plt.close()

    # Top 10 senders
    top_senders = address_df['sent'].sort_values(ascending=False).head(10)
    top_senders.plot(kind='bar', title='Top 10 Token Senders', figsize=(10, 6))
    plt.ylabel("Tokens Sent")
    plt.tight_layout()
    plt.savefig("top_senders_chart.png")
    plt.close()

    # Top 10 receivers
    top_receivers = address_df['received'].sort_values(ascending=False).head(10)
    top_receivers.plot(kind='bar', title='Top 10 Token Receivers', color='green', figsize=(10, 6))
    plt.ylabel("Tokens Received")
    plt.tight_layout()
    plt.savefig("top_receivers_chart.png")
    plt.close()

def main():
    print("Fetching data from API...")
    data = fetch_all_pages()
    print(f"Fetched {len(data)} records.")

    print("Cleaning and transforming data...")
    df = clean_and_transform(data)
    df.to_csv("clean_token_transfers.csv", index=False)
    print("Data saved to clean_token_transfers.csv")

    print("Generating charts...")
    save_charts(df)
    print("Charts saved. Analysis complete.")

if __name__ == "__main__":
    main()
