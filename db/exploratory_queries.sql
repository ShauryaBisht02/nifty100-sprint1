-- ============================================================
-- Nifty 100 Financial Intelligence Platform
-- Sprint 1, Day 7 — Exploratory SQL Queries
-- Run against: db/nifty100.db
-- All 10 queries tested and verified against the live database.
-- ============================================================

-- Q1: Row counts across all 10 tables (data foundation overview)
SELECT 'companies' AS table_name, COUNT(*) AS row_count FROM companies
UNION ALL SELECT 'profit_and_loss', COUNT(*) FROM profit_and_loss
UNION ALL SELECT 'balance_sheet', COUNT(*) FROM balance_sheet
UNION ALL SELECT 'cash_flow', COUNT(*) FROM cash_flow
UNION ALL SELECT 'documents', COUNT(*) FROM documents
UNION ALL SELECT 'sectors', COUNT(*) FROM sectors
UNION ALL SELECT 'stock_prices', COUNT(*) FROM stock_prices
UNION ALL SELECT 'market_cap', COUNT(*) FROM market_cap
UNION ALL SELECT 'financial_ratios', COUNT(*) FROM financial_ratios
UNION ALL SELECT 'peer_groups', COUNT(*) FROM peer_groups;

-- Q2: Null check — companies table (key descriptive/valuation fields)
SELECT
    SUM(CASE WHEN company_name IS NULL THEN 1 ELSE 0 END) AS null_company_name,
    SUM(CASE WHEN face_value   IS NULL THEN 1 ELSE 0 END) AS null_face_value,
    SUM(CASE WHEN roe_percentage IS NULL THEN 1 ELSE 0 END) AS null_roe_pct
FROM companies;

-- Q3: Null check — profit_and_loss (core P&L fields)
SELECT
    SUM(CASE WHEN sales      IS NULL THEN 1 ELSE 0 END) AS null_sales,
    SUM(CASE WHEN net_profit IS NULL THEN 1 ELSE 0 END) AS null_net_profit,
    SUM(CASE WHEN eps        IS NULL THEN 1 ELSE 0 END) AS null_eps
FROM profit_and_loss;

-- Q4: Null check — balance_sheet (core BS fields)
SELECT
    SUM(CASE WHEN total_assets      IS NULL THEN 1 ELSE 0 END) AS null_total_assets,
    SUM(CASE WHEN total_liabilities IS NULL THEN 1 ELSE 0 END) AS null_total_liabilities,
    SUM(CASE WHEN borrowings        IS NULL THEN 1 ELSE 0 END) AS null_borrowings
FROM balance_sheet;

-- Q5: Null check — cash_flow (core CF fields)
SELECT
    SUM(CASE WHEN operating_activity IS NULL THEN 1 ELSE 0 END) AS null_cfo,
    SUM(CASE WHEN net_cash_flow      IS NULL THEN 1 ELSE 0 END) AS null_net_cash_flow
FROM cash_flow;

-- Q6: Year coverage per company — profit_and_loss (min year, max year, count of years)
SELECT company_id, MIN(year) AS min_year, MAX(year) AS max_year, COUNT(*) AS year_count
FROM profit_and_loss
GROUP BY company_id
ORDER BY company_id;

-- Q7: Companies with less than 5 years of P&L history (DQ-16 coverage flag)
SELECT company_id, COUNT(*) AS years
FROM profit_and_loss
GROUP BY company_id
HAVING years < 5;

-- Q8: Duplicate (company_id, year) check — should return 0 rows post-dedup (DQ-02)
SELECT company_id, year, COUNT(*) AS dupes
FROM profit_and_loss
GROUP BY company_id, year
HAVING dupes > 1;

-- Q9: Orphan FK check — child rows whose company_id has no parent in companies (DQ-03)
SELECT 'profit_and_loss' AS tbl, COUNT(*) AS orphan_rows FROM profit_and_loss p
WHERE NOT EXISTS (SELECT 1 FROM companies c WHERE c.symbol = p.company_id)
UNION ALL
SELECT 'balance_sheet', COUNT(*) FROM balance_sheet b
WHERE NOT EXISTS (SELECT 1 FROM companies c WHERE c.symbol = b.company_id)
UNION ALL
SELECT 'cash_flow', COUNT(*) FROM cash_flow f
WHERE NOT EXISTS (SELECT 1 FROM companies c WHERE c.symbol = f.company_id);

-- Q10: Sector coverage — companies per broad_sector
SELECT broad_sector, COUNT(*) AS company_count
FROM sectors
GROUP BY broad_sector
ORDER BY company_count DESC;
