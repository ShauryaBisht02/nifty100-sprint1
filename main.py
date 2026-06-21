from src.etl.loader import load_excel

df = load_excel("data/raw/companies.xlsx")

print(df.head())