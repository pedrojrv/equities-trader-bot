import pandas as pd
from datetime import datetime

from pedrino.polygon_utils import ticker_details, aggregates


def test_create_stock_details_cols():
    test_df = pd.DataFrame(columns=["col1", "col2"])
    test_df = ticker_details._create_stock_details_cols(test_df)
    for col in ticker_details.TICKER_DETAIL_KEYS.values():
        assert col in test_df.columns


def test_append_ticker_details():
    from_date = datetime(2022, 9, 1, 6, 40, 0)
    agg = aggregates.get_agg('NVDA', from_date)
    agg = ticker_details.append_ticker_details(agg)

    assert len(agg.columns) == 16
    assert not agg.isnull().values.any()

