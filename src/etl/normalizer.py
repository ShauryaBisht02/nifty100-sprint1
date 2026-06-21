import pandas as pd

def normalize_ticker(ticker):
    if pd.isna(ticker):
        return None

    return str(ticker).strip().upper()


def normalize_year(year):
    if pd.isna(year):
        return None

    year = str(year).strip()

    months = {
        "Mar": "03",
        "Dec": "12",
        "Jun": "06",
        "Sep": "09"
    }

    try:
        month = year[:3]
        yr = year[-2:]

        if month in months:
            return f"20{yr}-{months[month]}"

    except:
        pass

    return year