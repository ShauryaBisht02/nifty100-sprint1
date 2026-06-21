# Sprint 1 Retrospective — Foundation & Data Engineering (Days 1–7)

**Sprint Goal:** Build `nifty100.db` from all 12 source files, zero CRITICAL DQ violations, ≥80% ETL coverage.
**Status:** ✅ Exit criteria met.

## What got done
- Project structure, venv, dependencies set up (D01)
- Excel loader (`header=1` core / `header=0` supporting) + `normalize_ticker()` / `normalize_year()` (D02)
- Schema validator with 16 DQ rules (D03)
- SQLite schema (10 tables, FK constraints) + `db/loader.py` (D04)
- Full load of all 12 source files → `nifty100.db` + `load_audit.csv`, 0 CRITICAL failures (D05)
- Manual DQ spot-check on 5 random companies across all time-series tables (D06)
- 10 exploratory SQL queries — row counts, nulls, year coverage, dedup/orphan checks, sector coverage (D07)

## Key metrics
- 100 companies in `companies` table (92 real + 8 placeholder for tickers present in financial data but absent from `companies.xlsx`)
- 1,263 profit_and_loss / 1,225 balance_sheet / 1,145 cash_flow rows loaded post-dedup + FK filtering
- `PRAGMA foreign_key_check` → clean, zero orphan rows
- No duplicate (company_id, year) pairs remain in any time-series table

## Findings / data quality notes (carry into Sprint 2)
1. **BAJFINANCE** — source `opm_percentage` field is corrupted (values like 1367–21417%, impossible range). Computed OPM (`operating_profit/sales×100`) gives sane 29–40%, matching NBFC sector benchmarks. **Ratio Engine must always use computed OPM, never the source field.**
2. **VBL** — zero rows in `balance_sheet` (confirmed genuine gap in raw `balancesheet.xlsx`, not a loader bug). VBL is also one of the 8 placeholder companies — overall coverage for it is partial. BS-dependent KPIs (D/E, ROCE, Asset Turnover) will be `None` for VBL.
3. **JIOFIN** — only 3 years of P&L history (DQ-16 flag, <5yr threshold). Recently-listed company; expected to have thin history. Exclude from long-window CAGR (5yr/10yr) calculations in Sprint 2; 3yr CAGR may still be computable if data allows.
4. **"TTM" year values** — `profit_and_loss.year` contains a `TTM` (Trailing Twelve Months) label for the latest row of several companies, which `normalize_year()` correctly leaves untouched since it isn't a fixed fiscal year-end. This technically doesn't match the strict `YYYY-MM` DQ-07 pattern. **Action for Sprint 2:** treat `TTM` rows as a separate "current/trailing" snapshot — exclude them from year-over-year CAGR math (they'd break the `(end/start)^(1/n)` logic) but keep them for "latest" KPI displays.
5. Minor null counts found (5 EPS nulls in P&L, 2 CFO/net-cash nulls in CF, ~9–10 nulls in companies' face_value/ROE for placeholder rows) — all expected and within WARNING-severity DQ tolerance, no rejection needed.

## Loader bugs found
**None.** All Day 6/7 anomalies trace to genuine source-data characteristics already anticipated by the DQ rule set, not defects in `loader.py`/`normalizer.py`.

## Carry-over / action items for Sprint 2 (Ratio Engine)
- [ ] Use computed OPM (not source field) for all companies, especially NBFCs/Financials
- [ ] Handle `TTM` rows separately from fiscal-year rows in CAGR functions
- [ ] Exclude JIOFIN (and any other <5yr company) from 5yr/10yr CAGR; allow 3yr only if ≥3 years present
- [ ] VBL: skip BS-dependent ratios gracefully (return `None`, don't crash)
- [ ] Bank/NBFC D/E carve-out (sector-relative benchmark) — confirm `sectors.broad_sector = 'Financials'` is used as the flag

## Sprint 1 sign-off
All Sprint 1 exit criteria met: 10 tables loaded, 0 CRITICAL DQ violations, FK integrity clean, DQ review complete, exploratory queries documented. **Proceeding to Sprint 2 — Financial Ratio Engine (Days 8–14).**
