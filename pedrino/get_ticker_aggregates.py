"""Module to get all available data for a given ticker."""
import pandas as pd
from pathlib import Path

from pedrino.data_utils import financials_utils, ticker_details_utils, trade_utils


def get_all_data_for_ticker(client, ticker, from_date=None, to_date=None, saving_dir=Path(".")):
    aggs = client.get_aggs(ticker, 1, "day", "2022-05-16", "2022-05-21", limit=4999)

    stock_price_history = pd.DataFrame({
        'open': [agg.open for agg in aggs],
        'high': [agg.high for agg in aggs],
        'low': [agg.low for agg in aggs],
        'close': [agg.close for agg in aggs],
        'volume': [agg.volume for agg in aggs],
        'vwap': [agg.vwap for agg in aggs],
        'transactions': [agg.transactions for agg in aggs],
    }, index=pd.to_datetime([agg.timestamp for agg in aggs], unit='ms'))

    stock_price_history = ticker_details_utils.append_ticker_details(client, ticker, stock_price_history)
    stock_price_history = financials_utils.append_stock_financials(client, ticker, stock_price_history)
    stock_price_history = trade_utils.append_trades_averages(client, ticker, stock_price_history)

    # stock_price_history.to_parquet()
    # stock_price_history.to_feather()
    stock_price_history.to_csv(saving_dir / f"{ticker}.csv")
