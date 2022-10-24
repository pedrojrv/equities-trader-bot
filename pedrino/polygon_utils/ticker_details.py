"""Utility to append ticker details to an aggregate dataframe."""
import numpy as np
import pandas as pd

from collections import OrderedDict
from datetime import datetime

from pedrino import client

TICKER_DETAIL_KEYS = OrderedDict({
    'list_date': 'list_date',
    'market_cap': 'mkt_cap',
    'share_class_shares_outstanding': 'shares_out',
    'sic_code': 'sic',
    'sic_description': 'sic_description',
    'total_employees': 'tot_empl',
    'weighted_shares_outstanding': 'w_shares_out',
})


def _create_stock_details_cols(stock_df: pd.DataFrame) -> pd.DataFrame:
    """Create empty columns for each stock detail."""
    for col in TICKER_DETAIL_KEYS.values():
        stock_df[col] = np.nan
    return stock_df


def append_ticker_details(stock_df: pd.DataFrame) -> pd.DataFrame:
    """Get ticker details and append information to data.

    Parameters
    ----------
    client : polygon.RESTClient
        Polygon client authorized to get data.
    ticker : str
        Ticker to get data for.
    stock_df : pandas.DataFrame
        DataFrame from which details are to be appended based on date index.

    Returns
    -------
    pandas.DataFrame
        Original DataFrame with details appended as new columns.
    """
    cl = client.get_client()
    if list(TICKER_DETAIL_KEYS.values())[0] not in stock_df.columns:
        stock_df = _create_stock_details_cols(stock_df)

    for idx, (ticker, timestamp) in enumerate(zip(stock_df.ticker, stock_df.date_s)):
        date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
        ticker_details = cl.get_ticker_details(ticker, date)
        for col in TICKER_DETAIL_KEYS:
            new_col = TICKER_DETAIL_KEYS[col]
            # stock_df.loc[stock_df['date_s'] == timestamp, new_col] = getattr(ticker_details, col)
            # stock_df.iloc[stock_df['date_s'] == timestamp, new_col] = getattr(ticker_details, col)
            stock_df.iloc[idx, stock_df.columns.get_loc(new_col)] = getattr(ticker_details, col)
    return stock_df
