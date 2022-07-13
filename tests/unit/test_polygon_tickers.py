import pytest
import pandas as pd
from pedrino.polygon_utils import tickers


@pytest.mark.skip("Remove skip fixture once Polygon account upgraded.")
def test_get_all(tmp_path):
    tickers.get_all(tmp_path)
    all_stocks_path = tmp_path / "all_stocks.csv"
    assert all_stocks_path.is_file()

    all_stocks = pd.read_csv(all_stocks_path)
    all_tickers = all_stocks.ticker.values
    for popular_tikcer in ['NVDA', 'AMD', 'FB']:
        assert popular_tikcer in all_tickers
