import pandas as pd
import os

CORE_PATH = "/home/shauryab/Downloads/n100-20260617T141341Z-3-001/n100"
SUPPORT_PATH = "/home/shauryab/Downloads/supporting datasets-20260617T141306Z-3-001/supporting datasets"

core_files = ["profitandloss.xlsx", "balancesheet.xlsx", "cashflow.xlsx",
              "documents.xlsx", "analysis.xlsx", "prosandcons.xlsx"]
support_files = ["sectors.xlsx", "stock_prices.xlsx", "market_cap.xlsx",
                  "financial_ratios.xlsx", "peer_groups.xlsx"]

for f in core_files:
    df = pd.read_excel(os.path.join(CORE_PATH, f), engine="openpyxl", header=1)
    print(f"\n=== {f} (header=1) ===")
    print(df.columns.tolist())
    print(df.head(2))

for f in support_files:
    df = pd.read_excel(os.path.join(SUPPORT_PATH, f), engine="openpyxl", header=0)
    print(f"\n=== {f} (header=0) ===")
    print(df.columns.tolist())
    print(df.head(2))