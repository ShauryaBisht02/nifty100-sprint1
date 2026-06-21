
import pandas as pd, sqlite3, os

CORE_PATH = "/home/shauryab/Downloads/n100-20260617T141341Z-3-001/n100"
df = pd.read_excel(os.path.join(CORE_PATH, "companies.xlsx"), engine="openpyxl", header=1)
print(df.columns.tolist())
print(df.head())

conn = sqlite3.connect("db/nifty100.db")
conn.execute("PRAGMA foreign_keys = ON;")
df.to_sql("companies", conn, if_exists="append", index=False)
