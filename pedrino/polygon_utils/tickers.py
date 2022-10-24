"""Get all supported tickers in Polygon."""
import argparse
import pandas as pd

from pathlib import Path
from typing import Optional
from polygon.rest.models import Market

from pedrino import client
from pedrino.polygon_utils import exchanges

pd.options.mode.chained_assignment = None


def get_all(saving_dir: Optional[Path] = None) -> pd.DataFrame:
    """Store all tickers supported in Polygon.

    Parameters
    ----------
    saving_dir : str
        Directory on which the CSV file will be saved

    Returns
    -------
    pandas.DataFrame
        Resulting DataFrame.
    """
    cl = client.get_client()
    stock_exchanges_dict = exchanges.get_stock_exchanges()

    # get all stocks for which there is information in Polygon
    all_polygon_tickers = cl.list_tickers(market=Market.STOCKS, type='CS', limit=1000000)
    valid_tickers = [ticker for ticker in all_polygon_tickers if ticker.locale == "us"]

    # All polygon tickers will form our base database, we will use its info to call other APIs for more info
    stock_info = pd.DataFrame({
        'ticker': [ticker.ticker for ticker in valid_tickers],
        'name': [ticker.name for ticker in valid_tickers],
        'exchange': [ticker.primary_exchange for ticker in valid_tickers],
        'locale': [ticker.locale for ticker in valid_tickers],
    })

    stock_info['exchange_name'] = stock_info['exchange'].apply(lambda x: stock_exchanges_dict[x])
    if saving_dir:
        stock_info.to_csv(saving_dir / "all_stocks.csv", index=False)
    return stock_info


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Queries and stores all tickers supported by Polygon.')
    parser.add_argument(
        "-s", "--saving-dir", action='store', help='Location on which the CSV file will be saved.', required=True)
    args = parser.parse_args()

    saving_dir = Path(args.saving_dir)
    get_all(saving_dir)
