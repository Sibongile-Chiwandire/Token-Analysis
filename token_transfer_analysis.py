
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

    # Top 10 senders
    top_senders = df.groupby('from.hash')['value'].sum().sort_values(ascending=False).head(10)
    top_senders.plot(kind='bar', title='Top 10 Token Senders', figsize=(10, 6))
    plt.ylabel("Tokens Sent")
    plt.tight_layout()
    plt.savefig("top_senders_chart.png")
    plt.close()

    # Top 10 receivers
    top_receivers = df.groupby('to.hash')['value'].sum().sort_values(ascending=False).head(10)
    top_receivers.plot(kind='bar', title='Top 10 Token Receivers', color='green', figsize=(10, 6))
    plt.ylabel("Tokens Received")
    plt.tight_layout()
    plt.savefig("top_receivers_chart.png")
    plt.close()

    # Mint and burn over time
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
