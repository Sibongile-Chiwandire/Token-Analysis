
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Token Transfer Dashboard", layout="wide")

st.title("📊 Blockchain Token Transfer Dashboard")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("clean_token_transfers.csv", parse_dates=["timestamp"])
    df["date"] = pd.to_datetime(df["timestamp"]).dt.date
    return df

df = load_data()

# KPIs
st.subheader("📌 Key Metrics")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Transactions", len(df))
with col2:
    st.metric("Total Tokens Transferred", f"{df['value'].sum():,.2f}")
with col3:
    st.metric("Total Volume (USD)", f"${df['usd_volume'].sum():,.2f}")

col4, col5, col6 = st.columns(3)
with col4:
    minted = df[df['type'] == 'token_minting']['value'].sum()
    st.metric("Tokens Minted", f"{minted:,.2f}")
with col5:
    burned = df[df['type'] == 'token_burning']['value'].sum()
    st.metric("Tokens Burned", f"{burned:,.2f}")
with col6:
    supply = minted - burned
    st.metric("Net Supply", f"{supply:,.2f}")

st.markdown("---")

# Daily transaction volume chart
st.subheader("📈 Daily Token Volume")
daily_df = df.groupby(["token.symbol", "date"])["value"].sum().unstack(0).fillna(0)
st.line_chart(daily_df)

# Top senders and receivers using matplotlib for proper labels
st.subheader("🏆 Top 10 Senders & Receivers")

top_senders = df.groupby("from.hash")["value"].sum().sort_values(ascending=False).head(10)
top_receivers = df.groupby("to.hash")["value"].sum().sort_values(ascending=False).head(10)

col7, col8 = st.columns(2)

with col7:
    st.subheader("Top 10 Token Senders")
    fig, ax = plt.subplots()
    top_senders_df = top_senders.reset_index()
    ax.barh(top_senders_df["from.hash"], top_senders_df["value"], color="skyblue")
    ax.set_xlabel("Tokens Sent")
    ax.set_ylabel("Sender Address")
    ax.set_title("Top Senders")
    ax.invert_yaxis()
    st.pyplot(fig)

with col8:
    st.subheader("Top 10 Token Receivers")
    fig, ax = plt.subplots()
    top_receivers_df = top_receivers.reset_index()
    ax.barh(top_receivers_df["to.hash"], top_receivers_df["value"], color="lightgreen")
    ax.set_xlabel("Tokens Received")
    ax.set_ylabel("Receiver Address")
    ax.set_title("Top Receivers")
    ax.invert_yaxis()
    st.pyplot(fig)

# Minting and burning trends
st.subheader("🔥 Minting vs Burning Over Time")
mint_df = df[df["type"] == "token_minting"].groupby("date")["value"].sum()
burn_df = df[df["type"] == "token_burning"].groupby("date")["value"].sum()

mint_burn_df = pd.DataFrame({"Minted": mint_df, "Burned": burn_df}).fillna(0)
st.line_chart(mint_burn_df)

st.markdown("---")
st.caption("Built with ❤️ by Sibongile Chiwandire for the Data Engineer Assessment")
