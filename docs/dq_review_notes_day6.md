# Sprint 1 — Day 6: Data Quality Review Notes

**Date:** 2026-06-21
**Reviewer:** Shaurya Bisht
**Scope:** Manual cross-check of 5 randomly sampled companies across all time-series tables (profit_and_loss, balance_sheet, cash_flow) in `nifty100.db`.

## Sample (random seed)
TATACONSUM, BAJFINANCE, ADANIGREEN, VBL, HAL

## Checks performed (per company)
- Coverage: years present in P&L / BS / CF (DQ-16, needs ≥5)
- DQ-06: no non-positive sales
- DQ-05: OPM cross-check — `opm_percentage` (source) vs computed `operating_profit/sales×100`
- DQ-04: Balance sheet balance — `|total_assets − total_liabilities| / total_assets < 1%`
- DQ-09: Net cash check — `net_cash_flow` vs `CFO+CFI+CFF` (±₹10 Cr tolerance)

## Results

| Company | P&L / BS / CF years | DQ-06 | DQ-05 (OPM) | DQ-04 (BS) | DQ-09 (Cash) |
|---|---|---|---|---|---|
| TATACONSUM | 13 / 13 / 12 | ✅ pass | ✅ 0/13 mismatch | ✅ 0/13 | ✅ 0/12 |
| BAJFINANCE | 11 / 11 / 10 | ✅ pass | ⚠️ **11/11 mismatch** | ✅ 0/11 | ✅ 0/10 |
| ADANIGREEN | 9 / 9 / 8 | ✅ pass | ✅ 0/9 mismatch | ✅ 0/9 | ✅ 0/8 |
| VBL | 13 / **0** / 12 | ✅ pass | ✅ 0/13 mismatch | n/a | ✅ 0/12 |
| HAL | 13 / 10 / 8 | ✅ pass | ✅ 0/13 mismatch | ✅ 0/10 | ✅ 0/8 |

## Findings

**1. BAJFINANCE — source `opm_percentage` field is corrupted (not a loader bug).**
Source values are 1367–21417 (i.e. nowhere near a valid 0–100% range), while computed OPM (`operating_profit/sales×100`) gives sensible 29–40%, consistent with the documented NBFC sector benchmark (25–45%, see KPI Reference). Raw source data quality issue, not introduced by the loader. **Action:** per DQ-05 rule, downstream Ratio Engine (Task/Sprint 2) must always use the *computed* OPM, never the source `opm_percentage` field. No loader fix needed.

**2. VBL — zero rows in balance_sheet (genuine source data gap, not a bug).**
Confirmed by reading `data/raw/balancesheet.xlsx` directly: VBL has 0 rows in the raw file (it does have 13 P&L years and 12 CF years). This is consistent with VBL also being one of the 9 missing-from-`companies.xlsx` placeholder tickers — its overall data coverage across the platform is incomplete. **Action:** flag VBL as a DQ-16 partial-coverage company for balance_sheet specifically; downstream balance-sheet-dependent KPIs (D/E, ROCE, Asset Turnover) will be `None` for VBL. No loader fix needed — correctly reflects source data.

**3. Everyone else (TATACONSUM, ADANIGREEN, HAL):** all DQ checks pass clean, no anomalies.

## Loader bugs found
None. All discrepancies trace back to genuine source-data characteristics (NBFC OPM field semantics, VBL coverage gap), already anticipated by DQ-05/DQ-16 rules in the spec. **No re-run of `make load` required.**

## Sign-off
Day 6 DQ review complete. Proceeding to Day 7 (10 exploratory SQL queries + Sprint 1 retro).
