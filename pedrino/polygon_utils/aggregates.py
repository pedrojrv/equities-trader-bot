"""Module to get all available data for a given ticker."""
import pandas as pd
from datetime import datetime

from pedrino import client


def get_agg(ticker: str, from_date: datetime, to_date: datetime) -> pd.DataFrame:
    cl = client.get_client()
    aggs = cl.get_aggs(ticker, 1, "minute", from_date, to_date, limit=50000)

    stock_price_history = pd.DataFrame({
        'open': [agg.open for agg in aggs],
        'high': [agg.high for agg in aggs],
        'low': [agg.low for agg in aggs],
        'close': [agg.close for agg in aggs],
        'volume': [agg.volume for agg in aggs],
        'vwap': [agg.vwap for agg in aggs],
        'transactions': [agg.transactions for agg in aggs],
    }, index=pd.to_datetime([agg.timestamp for agg in aggs], unit='ms'))
    stock_price_history['ticker'] = ticker
    return stock_price_history
