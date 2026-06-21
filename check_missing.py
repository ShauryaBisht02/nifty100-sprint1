import pandas as pd
import sqlite3
import os

CORE_PATH = "/home/shauryab/Downloads/n100-20260617T141341Z-3-001/n100"
SUPPORT_PATH = "/home/shauryab/Downloads/supporting datasets-20260617T141306Z-3-001/supporting datasets"

conn = sqlite3.connect("db/nifty100.db")
existing = set(r[0] for r in conn.execute("SELECT symbol FROM companies"))
print(f"Total companies in DB: {len(existing)}")

checks = [
    (CORE_PATH, "profitandloss.xlsx", 1),
    (CORE_PATH, "balancesheet.xlsx", 1),
    (CORE_PATH, "cashflow.xlsx", 1),
    (CORE_PATH, "documents.xlsx", 1),
    (CORE_PATH, "analysis.xlsx", 1),
    (CORE_PATH, "prosandcons.xlsx", 1),
    (SUPPORT_PATH, "financial_ratios.xlsx", 0),
]

for folder, file, header in checks:
    df = pd.read_excel(os.path.join(folder, file), engine="openpyxl", header=header)
    ids = set(df["company_id"].dropna().unique())
    missing = ids - existing
    print(f"\n{file}: unique company_id={len(ids)}, missing from companies={len(missing)}")
    if missing:
        print(sorted(missing)[:20])