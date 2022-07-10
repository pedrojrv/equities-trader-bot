"""Utility to append ticker details to an aggregate dataframe."""
import numpy as np
from collections import OrderedDict

TICKER_DETAIL_KEYS = OrderedDict({
    'list_date': 'list_date',
    'market_cap': 'mk_cap',
    'share_class_shares_outstanding': 'shares_out',
    'sic_code': 'sic',
    'sic_description': 'sic_description',
    'total_employees': 'tot_empl',
    'weighted_shares_outstanding': 'w_shares_out',
})


def append_ticker_details(client, ticker, stock_df):
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
    for col in TICKER_DETAIL_KEYS:
        new_col = TICKER_DETAIL_KEYS[col]
        stock_df[new_col] = np.nan

    for date in stock_df.index:
        datetime = date.strftime('%Y-%m-%d')
        ticker_details = client.get_ticker_details(ticker, date=datetime)
        for col in TICKER_DETAIL_KEYS:
            new_col = TICKER_DETAIL_KEYS[col]
            stock_df.at[date, new_col] = getattr(ticker_details, col)
    return stock_df
