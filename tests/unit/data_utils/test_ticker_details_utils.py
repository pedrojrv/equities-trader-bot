import pandas as pd

from pedrino.polygon_utils import ticker_details


def test_create_stock_details_cols():
    df = pd.DataFrame()
    df = ticker_details._create_stock_details_cols(df)
    for column in ticker_details.TICKER_DETAIL_KEYS.values():
        assert column in df.columns


def test_append_ticker_details():
    ticker = "NVDA"
    date = "2022-05-27"
    df = pd.DataFrame({'date': [date]}).set_index('date')
    df.index = pd.to_datetime(df.index)
    df = ticker_details.append_ticker_details(ticker, df)

    assert df.isna().sum().sum() == 0
    assert df.sic_description[0] == 'SEMICONDUCTORS & RELATED DEVICES'
    assert len(df) == 1
