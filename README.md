
# Blockchain Token Transfer Analysis

## Overview
This project analyzes token transactions from a blockchain network using a REST API. It includes data extraction, cleaning, aggregation, and visual insights.

---

## Files Included

| File Name                     | Description |
|------------------------------|-------------|
| `token_transfer_analysis.py` | Python script to fetch, clean, and analyze blockchain data |
| `clean_token_transfers.csv`  | Cleaned dataset of token transfers |
| `daily_volume_chart.png`     | Daily transaction volume per token |
| `top_senders_chart.png`      | Top 10 token-sending addresses |
| `top_receivers_chart.png`    | Top 10 token-receiving addresses |
| `mint_burn_chart.png`        | Daily token minting and burning trends |
| `Insights_Report.md`         | Summary report with approach and key insights |
| `README.md`                  | This instruction file |

---

## How to Run

### Option 1: Python Script

1. Ensure Python 3.7+ is installed
2. Install dependencies:
```bash
pip install pandas requests matplotlib seaborn
```
3. Run the script:
```bash
python token_transfer_analysis.py
```
This will:
- Fetch token transfers from the API
- Clean and convert the data
- Save results to `clean_token_transfers.csv`
- Generate and save charts as `.png` files

---

### Charts Explained

- **daily_volume_chart.png**  
  Shows token volume per day per symbol to help track activity over time.

- **top_senders_chart.png**  
  Top 10 addresses that have sent the most tokens.

- **top_receivers_chart.png**  
  Top 10 addresses that have received the most tokens.

- **mint_burn_chart.png**  
  Compares the number of tokens minted vs burned daily.

---

## Notes

- The script uses the XCAP blockchain token transfers API with pagination.
- All values are normalized using `token.decimals` and converted to USD using the `token.exchange_rate`.

---

## Contact

For questions or improvements, feel free to reach out.
