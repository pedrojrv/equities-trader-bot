import pandas as pd

from pedrino.data_utils import financials_utils


def test_create_financial_columns():
    df = pd.DataFrame()
    df = financials_utils._create_financial_columns(df)
    for column in financials_utils.ALL_FINANCIAL_COLS:
        assert column in df.columns


