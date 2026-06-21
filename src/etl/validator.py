import pandas as pd
import os

# =====================================================
# CONFIG
# =====================================================

DATA_FOLDER = "data/raw"

FILES = [
    "balancesheet.xlsx",
    "analysis.xlsx",
    "cashflow.xlsx",
    "companies.xlsx",
    "documents.xlsx",
    "prosandcons.xlsx",
    "profitandloss.xlsx"
]

# =====================================================
# FAILURE LOGGER
# =====================================================

failures = []

def log_failure(rule_id, severity, file_name,
                row_no, column_name,
                invalid_value, reason):

    failures.append({
        "rule_id": rule_id,
        "severity": severity,
        "file_name": file_name,
        "row_number": row_no,
        "column_name": column_name,
        "invalid_value": invalid_value,
        "reason": reason
    })

# =====================================================
# LOAD FILES
# =====================================================

dataframes = {}

for file in FILES:

    path = os.path.join(DATA_FOLDER, file)

    try:
        df = pd.read_excel(path)

        dataframes[file] = df

        print(f"Loaded {file} | Rows={len(df)} | Cols={len(df.columns)}")

    except Exception as e:

        log_failure(
            "DQ-00",
            "CRITICAL",
            file,
            "",
            "",
            "",
            f"File Load Error: {e}"
        )

# =====================================================
# DQ-01 Missing Values in Mandatory Columns Only
# =====================================================

mandatory_columns = ["id", "company_id"]

for file, df in dataframes.items():

    for col in mandatory_columns:

        if col in df.columns:

            bad_rows = df[df[col].isna()]

            for idx in bad_rows.index:

                log_failure(
                    "DQ-01",
                    "CRITICAL",
                    file,
                    idx,
                    col,
                    "",
                    "Missing mandatory value"
                )

# =====================================================
# DQ-02 Duplicate Rows
# =====================================================

for file, df in dataframes.items():

    duplicates = df[df.duplicated()]

    for idx in duplicates.index:

        log_failure(
            "DQ-02",
            "WARNING",
            file,
            idx,
            "",
            "",
            "Duplicate row"
        )

# =====================================================
# DQ-03 Empty Strings
# =====================================================

for file, df in dataframes.items():

    for col in df.columns:

        if df[col].dtype == object:

            bad_rows = df[
                df[col].astype(str).str.strip() == ""
            ]

            for idx in bad_rows.index:

                log_failure(
                    "DQ-03",
                    "WARNING",
                    file,
                    idx,
                    col,
                    "",
                    "Empty string"
                )

# =====================================================
# DQ-04 Duplicate ID
# =====================================================

for file, df in dataframes.items():

    if "id" in df.columns:

        dup_ids = df[df["id"].duplicated()]

        for idx in dup_ids.index:

            log_failure(
                "DQ-04",
                "CRITICAL",
                file,
                idx,
                "id",
                dup_ids.loc[idx, "id"],
                "Duplicate ID"
            )

# =====================================================
# DQ-05 Missing ID
# =====================================================

for file, df in dataframes.items():

    if "id" in df.columns:

        bad_rows = df[df["id"].isna()]

        for idx in bad_rows.index:

            log_failure(
                "DQ-05",
                "CRITICAL",
                file,
                idx,
                "id",
                "",
                "Missing ID"
            )

# =====================================================
# DQ-06 Missing company_id
# =====================================================

for file, df in dataframes.items():

    if "company_id" in df.columns:

        bad_rows = df[df["company_id"].isna()]

        for idx in bad_rows.index:

            log_failure(
                "DQ-06",
                "CRITICAL",
                file,
                idx,
                "company_id",
                "",
                "Missing company_id"
            )

# =====================================================
# DQ-07 Foreign Key Check
# =====================================================

if "companies.xlsx" in dataframes:

    companies_df = dataframes["companies.xlsx"]

    if "company_id" in companies_df.columns:

        valid_ids = set(
            companies_df["company_id"]
            .dropna()
            .astype(str)
        )

        for file, df in dataframes.items():

            if file == "companies.xlsx":
                continue

            if "company_id" in df.columns:

                for idx, value in df["company_id"].items():

                    if pd.notna(value):

                        if str(value) not in valid_ids:

                            log_failure(
                                "DQ-07",
                                "CRITICAL",
                                file,
                                idx,
                                "company_id",
                                value,
                                "Foreign Key Not Found"
                            )

# =====================================================
# DQ-08 Duplicate Column Names
# =====================================================

for file, df in dataframes.items():

    if len(df.columns) != len(set(df.columns)):

        log_failure(
            "DQ-08",
            "CRITICAL",
            file,
            "",
            "",
            "",
            "Duplicate Column Names"
        )

# =====================================================
# DQ-09 Empty Dataset
# =====================================================

for file, df in dataframes.items():

    if len(df) == 0:

        log_failure(
            "DQ-09",
            "CRITICAL",
            file,
            "",
            "",
            "",
            "Empty Dataset"
        )

# =====================================================
# DQ-10 Negative Numeric Values
# =====================================================

for file, df in dataframes.items():

    numeric_cols = df.select_dtypes(include="number").columns

    for col in numeric_cols:

        bad_rows = df[df[col] < 0]

        for idx in bad_rows.index:

            log_failure(
                "DQ-10",
                "WARNING",
                file,
                idx,
                col,
                bad_rows.loc[idx, col],
                "Negative Value"
            )

# =====================================================
# DQ-11 Entire Column Null
# =====================================================

for file, df in dataframes.items():

    for col in df.columns:

        if df[col].isna().all():

            log_failure(
                "DQ-11",
                "WARNING",
                file,
                "",
                col,
                "",
                "Entire Column Null"
            )

# =====================================================
# DQ-12 Leading Spaces
# =====================================================

for file, df in dataframes.items():

    for col in df.columns:

        if df[col].dtype == object:

            bad_rows = df[
                df[col].astype(str).str.startswith(" ")
            ]

            for idx in bad_rows.index:

                log_failure(
                    "DQ-12",
                    "WARNING",
                    file,
                    idx,
                    col,
                    bad_rows.loc[idx, col],
                    "Leading Space"
                )

# =====================================================
# DQ-13 Trailing Spaces
# =====================================================

for file, df in dataframes.items():

    for col in df.columns:

        if df[col].dtype == object:

            bad_rows = df[
                df[col].astype(str).str.endswith(" ")
            ]

            for idx in bad_rows.index:

                log_failure(
                    "DQ-13",
                    "WARNING",
                    file,
                    idx,
                    col,
                    bad_rows.loc[idx, col],
                    "Trailing Space"
                )

# =====================================================
# DQ-14 Single Unique Value
# =====================================================

for file, df in dataframes.items():

    for col in df.columns:

        if df[col].nunique(dropna=True) == 1:

            log_failure(
                "DQ-14",
                "WARNING",
                file,
                "",
                col,
                "",
                "Only One Unique Value"
            )

# =====================================================
# DQ-15 Blank Column Name
# =====================================================

for file, df in dataframes.items():

    for col in df.columns:

        if str(col).strip() == "":

            log_failure(
                "DQ-15",
                "CRITICAL",
                file,
                "",
                "",
                "",
                "Blank Column Name"
            )

# =====================================================
# DQ-16 Very Long Text
# =====================================================

for file, df in dataframes.items():

    for col in df.columns:

        if df[col].dtype == object:

            for idx, value in df[col].dropna().items():

                if len(str(value)) > 500:

                    log_failure(
                        "DQ-16",
                        "WARNING",
                        file,
                        idx,
                        col,
                        "TEXT_TOO_LONG",
                        "Length > 500"
                    )

# =====================================================
# SAVE OUTPUT
# =====================================================

report = pd.DataFrame(failures)

report.to_csv(
    "validation_failures.csv",
    index=False
)

print("\n================================")
print("Validation Complete")
print("Total Failures :", len(report))
print("Output : validation_failures.csv")
print("================================")