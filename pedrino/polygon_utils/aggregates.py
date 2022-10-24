"""Module to get all available data for a given ticker."""
import pandas as pd
from typing import Optional
from datetime import datetime

from pedrino import client


def get_agg(ticker: str, from_date: datetime, to_date: Optional[datetime] = None) -> pd.DataFrame:
    """Get minute-level aggregates for a given ticker.

    It is a wrapper around polygon.RESTClient.get_aggs().

    Parameters
    ----------
    ticker : str
    from_date : datetime
        Date time at which to start aggregate.
    to_date : Optional[datetime], optional
        Date time at which to end aggregate, by default None. If None, the end date is the same as from_date.

    Returns
    -------
    pd.DataFrame
        Resulting aggregate data formatted as a pandas DataFrame.
    """
    cl = client.get_client()
    if not to_date:
        to_date = from_date

    aggs = cl.get_aggs(ticker, 1, "minute", from_date, to_date, limit=50000)

    stock_price_history = pd.DataFrame({
        'date_s': [int(agg.timestamp/1000) for agg in aggs],
        'open': [agg.open for agg in aggs],
        'high': [agg.high for agg in aggs],
        'low': [agg.low for agg in aggs],
        'close': [agg.close for agg in aggs],
        'volume': [agg.volume for agg in aggs],
        'vwap': [agg.vwap for agg in aggs],
        'transactions': [agg.transactions for agg in aggs],
    })

    stock_price_history['ticker'] = ticker
    return stock_price_history
