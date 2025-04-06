
# Insights Report: Blockchain Token Transfer Analysis

**Candidate:** Sibongile Chiwandire  
**Date:** April 2025

---

## 🔍 Approach Overview

This project analyzes token transactions on the XCAP blockchain network via a REST API. The goal is to extract data, clean and transform it, compute key blockchain metrics, and visualize trends for decision-making.

---

## 🛠️ Tools Used

- **Python**: Core scripting language
- **pandas**: Data manipulation
- **matplotlib & seaborn**: Visualization
- **requests**: API data extraction

---

## ✅ Task Breakdown

### 1. Data Extraction & Processing
- Connected to `XCAP Token Transfers API` and handled pagination.
- Extracted fields: token symbol, value, from/to address, type, timestamp, exchange rate.
- Normalized token values using `token.decimals`.
- Converted timestamps and ensured data quality (duplicates and null handling).

### 2. Key Metrics

| Metric                     | Description                                  |
|---------------------------|----------------------------------------------|
| Total Asset Supply        | Minted tokens minus burned tokens            |
| Number of Unique Tokens   | Distinct token symbols                       |
| Number of Transactions    | Count of all token transfers                 |
| Tokens Minted             | Sum of values where type = `token_minting`   |
| Tokens Burned             | Sum of values where type = `token_burning`   |
| Tokens Transferred        | Sum where type = `token_transfer`            |
| Total Transaction Volume  | USD Volume = token amount * exchange rate    |

### 3. Address Analysis

- **Top Holders**: Net = (Minted - Burned) + (Received - Sent)
- **Top Senders**: Grouped by `from.hash`
- **Top Receivers**: Grouped by `to.hash`

### 4. Transaction Trends & Insights

- **Daily Volume by Token**: Shows activity trend by token
- **Mint/Burn Spikes**: Visualized minting vs burning patterns
- **Anomalies Detected**:
  - Spikes in minting may signal reward distributions or inflation
  - Burn spikes could indicate token control mechanisms

---

## 📌 Assumptions

- Exchange rate reflects value at the exact moment of the transaction.
- API returns complete and accurate historical data.

---

## 📊 Summary of Visuals

- **daily_volume_chart.png**: Daily token activity
- **top_senders_chart.png**: Highest token outflows
- **top_receivers_chart.png**: Highest inflows
- **mint_burn_chart.png**: Supply changes and tokenomics

---

## 💡 Final Thoughts

This project demonstrates:
- Strong REST API interaction
- Robust data cleaning and transformation
- Accurate metric calculation
- Meaningful visual storytelling

Ready for production enhancements like:
- Automated pipeline (Airflow/Step Functions)
- Dashboard deployment (Streamlit/Power BI)

