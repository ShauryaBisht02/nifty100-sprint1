import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../")
    )
)
from src.etl.normalizer import normalize_ticker
from src.etl.normalizer import normalize_year


def test_ticker():
    assert normalize_ticker(" tcs ") == "TCS"
    assert normalize_ticker("infy") == "INFY"


def test_year():
    assert normalize_year("Mar-23") == "2023-03"
    assert normalize_year("Dec-24") == "2024-12"
from src.etl.normalizer import normalize_ticker
from src.etl.normalizer import normalize_year


# --------------------------
# TICKER TESTS (20 Cases)
# --------------------------

def test_ticker_01():
    assert normalize_ticker(" tcs ") == "TCS"

def test_ticker_02():
    assert normalize_ticker("infy") == "INFY"

def test_ticker_03():
    assert normalize_ticker("RELIANCE") == "RELIANCE"

def test_ticker_04():
    assert normalize_ticker(" hdfc ") == "HDFC"

def test_ticker_05():
    assert normalize_ticker("icici") == "ICICI"

def test_ticker_06():
    assert normalize_ticker("sbIN") == "SBIN"

def test_ticker_07():
    assert normalize_ticker("lt") == "LT"

def test_ticker_08():
    assert normalize_ticker("wipro") == "WIPRO"

def test_ticker_09():
    assert normalize_ticker("asianpaint") == "ASIANPAINT"

def test_ticker_10():
    assert normalize_ticker(" titan ") == "TITAN"

def test_ticker_11():
    assert normalize_ticker("abc123") == "ABC123"

def test_ticker_12():
    assert normalize_ticker("A1B2C3") == "A1B2C3"

def test_ticker_13():
    assert normalize_ticker("   xyz") == "XYZ"

def test_ticker_14():
    assert normalize_ticker("xyz   ") == "XYZ"

def test_ticker_15():
    assert normalize_ticker("xYz") == "XYZ"

def test_ticker_16():
    assert normalize_ticker("") == ""

def test_ticker_17():
    assert normalize_ticker(" ") == ""

def test_ticker_18():
    assert normalize_ticker("NESTLEIND") == "NESTLEIND"

def test_ticker_19():
    assert normalize_ticker("bajajfin") == "BAJAJFIN"

def test_ticker_20():
    assert normalize_ticker("tatamotors") == "TATAMOTORS"


# --------------------------
# YEAR TESTS (20 Cases)
# --------------------------

def test_year_01():
    assert normalize_year("Mar-23") == "2023-03"

def test_year_02():
    assert normalize_year("Dec-24") == "2024-12"

def test_year_03():
    assert normalize_year("Jun-22") == "2022-06"

def test_year_04():
    assert normalize_year("Sep-21") == "2021-09"

def test_year_05():
    assert normalize_year("Mar-20") == "2020-03"

def test_year_06():
    assert normalize_year("Dec-19") == "2019-12"

def test_year_07():
    assert normalize_year("Jun-18") == "2018-06"

def test_year_08():
    assert normalize_year("Sep-17") == "2017-09"

def test_year_09():
    assert normalize_year("Mar-16") == "2016-03"

def test_year_10():
    assert normalize_year("Dec-15") == "2015-12"

def test_year_11():
    assert normalize_year("Jun-14") == "2014-06"

def test_year_12():
    assert normalize_year("Sep-13") == "2013-09"

def test_year_13():
    assert normalize_year("Mar-12") == "2012-03"

def test_year_14():
    assert normalize_year("Dec-11") == "2011-12"

def test_year_15():
    assert normalize_year("Jun-10") == "2010-06"

def test_year_16():
    assert normalize_year("Sep-09") == "2009-09"

def test_year_17():
    assert normalize_year("2024") == "2024"

def test_year_18():
    assert normalize_year("FY24") == "FY24"

def test_year_19():
    assert normalize_year("") == ""

def test_year_20():
    assert normalize_year("Random") == "Random"    