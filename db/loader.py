import sqlite3
import pandas as pd
import json
import os
import time
import traceback
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = "db/nifty100.db"
SCHEMA_PATH = "db/schema.sql"
from src.etl.normalizer import normalize_ticker, normalize_year  

CORE_PATH = "data/raw"                  
SUPPORT_PATH = "data/supporting"        
audit_log = []

DEDUP_KEYS = {
    "companies": ["symbol"],
    "profit_and_loss": ["company_id", "year"],
    "balance_sheet": ["company_id", "year"],
    "cash_flow": ["company_id", "year"],
    "financial_ratios": ["company_id", "year"],
    "market_cap": ["company_id", "year"],
    "stock_prices": ["company_id", "date"],
}


def get_connection():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    with open(SCHEMA_PATH, "r") as f:
        conn.executescript(f.read())
    return conn


def load_core(file_name):
    path = os.path.join(CORE_PATH, file_name)
    df = pd.read_excel(path, header=1)

    if file_name == "companies.xlsx":
        df["id"] = df["id"].apply(normalize_ticker)
    elif "id" in df.columns:
        df = df.drop(columns=["id"])

    if "company_id" in df.columns:
        df["company_id"] = df["company_id"].apply(normalize_ticker)

    if "year" in df.columns:
        df["year"] = df["year"].apply(normalize_year)

    return df


def load_support(file_name):
    path = os.path.join(SUPPORT_PATH, file_name)
    df = pd.read_excel(path, header=0)

    if "id" in df.columns:
        df = df.drop(columns=["id"])
    if "company_id" in df.columns:
        df["company_id"] = df["company_id"].apply(normalize_ticker)

    return df


def load_documents_group():
    rows = []

    docs = load_core("documents.xlsx")
    for _, r in docs.iterrows():
        rows.append({
            "company_id": r.get("company_id"),
            "doc_type": "annual_report",
            "content": json.dumps({"year": r.get("Year"), "url": r.get("Annual_Report")}, default=str)
        })

    analysis = load_core("analysis.xlsx")
    for _, r in analysis.iterrows():
        rows.append({
            "company_id": r.get("company_id"),
            "doc_type": "analysis",
            "content": json.dumps({
                "compounded_sales_growth": r.get("compounded_sales_growth"),
                "compounded_profit_growth": r.get("compounded_profit_growth"),
                "stock_price_cagr": r.get("stock_price_cagr"),
                "roe": r.get("roe"),
            }, default=str)
        })

    pc = load_core("prosandcons.xlsx")
    for _, r in pc.iterrows():
        rows.append({
            "company_id": r.get("company_id"),
            "doc_type": "pros_cons",
            "content": json.dumps({"pros": r.get("pros"), "cons": r.get("cons")}, default=str)
        })

    return pd.DataFrame(rows)


def get_valid_company_ids(conn):
    try:
        return set(pd.read_sql("SELECT symbol FROM companies", conn)["symbol"])
    except Exception:
        return set()


def insert_df(df, table_name, conn, file_name):
    start = time.time()
    rejected = 0
    status = "SUCCESS"
    error = ""
    rows_loaded = 0

    try:
        if table_name in DEDUP_KEYS:
            keys = DEDUP_KEYS[table_name]
            if all(k in df.columns for k in keys):
                df = df.drop_duplicates(subset=keys, keep="last")

        if table_name != "companies" and "company_id" in df.columns:
            valid_ids = get_valid_company_ids(conn)
            mask = df["company_id"].isin(valid_ids)
            rejected = int((~mask).sum())
            df = df[mask]

        df.to_sql(table_name, conn, if_exists="append", index=False)
        rows_loaded = len(df)

    except Exception as e:
        status = "FAIL"
        error = str(e)
        print(f"\n❌ {file_name} -> {table_name}: {error}")
        print(traceback.format_exc())

    runtime = round(time.time() - start, 3)
    audit_log.append({
        "file_name": file_name,
        "table_name": table_name,
        "rows_loaded": rows_loaded,
        "rejected_rows": rejected,
        "runtime_sec": runtime,
        "status": status,
        "error": error
    })


def save_audit():
    audit_df = pd.DataFrame(audit_log)
    audit_df.to_csv("load_audit.csv", index=False)
    print(audit_df.to_string(index=False))


def run_loader():
    conn = get_connection()

    companies = load_core("companies.xlsx")
    companies = companies.rename(columns={"id": "symbol"})
    insert_df(companies, "companies", conn, "companies.xlsx")

    missing_symbols = ["ULTRACEMCO", "UNIONBANK", "UNITDSPR", "VBL", "VEDL", "WIPRO", "ZOMATO", "ZYDUSLIFE"]
    placeholder_df = pd.DataFrame({
        "symbol": missing_symbols,
        "company_logo": [None] * len(missing_symbols),
        "company_name": missing_symbols,
        "chart_link": [None] * len(missing_symbols),
        "about_company": [None] * len(missing_symbols),
        "website": [None] * len(missing_symbols),
        "nse_profile": [None] * len(missing_symbols),
        "bse_profile": [None] * len(missing_symbols),
        "face_value": [None] * len(missing_symbols),
        "book_value": [None] * len(missing_symbols),
        "roce_percentage": [None] * len(missing_symbols),
        "roe_percentage": [None] * len(missing_symbols),
    })
    insert_df(placeholder_df, "companies", conn, "missing_companies")

    core_files = {
        "profitandloss.xlsx": "profit_and_loss",
        "balancesheet.xlsx": "balance_sheet",
        "cashflow.xlsx": "cash_flow",
    }
    for file_name, table_name in core_files.items():
        df = load_core(file_name)
        insert_df(df, table_name, conn, file_name)

    docs_df = load_documents_group()
    insert_df(docs_df, "documents", conn, "documents_group")

    support_files = {
        "sectors.xlsx": "sectors",
        "stock_prices.xlsx": "stock_prices",
        "market_cap.xlsx": "market_cap",
        "financial_ratios.xlsx": "financial_ratios",
        "peer_groups.xlsx": "peer_groups",
    }
    for file_name, table_name in support_files.items():
        df = load_support(file_name)
        insert_df(df, table_name, conn, file_name)

    conn.commit()
    conn.close()
    save_audit()
    print("\n🎯 DAY 5 COMPLETED")


if __name__ == "__main__":
    run_loader()