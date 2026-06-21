import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

df = pd.read_excel(
    "/home/shauryab/Downloads/n100-20260617T141341Z-3-001/n100/profitandloss.xlsx",
    header=1
)

print(df.columns.tolist())
print(df.dtypes)

try:
    df.to_sql(
        "profit_and_loss",
        conn,
        if_exists="append",
        index=False
    )
except Exception as e:
    print(type(e))
    print(repr(e))