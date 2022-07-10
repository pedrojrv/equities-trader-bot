"""Utility module to get trade related data."""
import numpy as np


def _get_average_data_trades(trades_iterable):
    average_price = []
    total_volume = 0
    num_trades = 0
    for trade in trades_iterable:
        average_price.append(trade.price)
        total_volume += trade.size
        num_trades += 1
    average_price = average_price / num_trades
    return average_price, total_volume, num_trades


def append_trades_averages(client, ticker, stock_df):
    """Append trade data for each date-index in the dataframe.

    Parameters
    ----------
    client : polygon.RESTClient
        Authorized polygon client.
    ticker : str
        Company ticker symbol.
    stock_df : pandas.DataFrame
        DataFrame to append trade average information to.

    Returns
    -------
    pandas.DataFrame
        _description_
    """
    for col in ['trade_avg_price', 'trade_avg_vol', 'trade_nums']:
        stock_df[col] = np.nan

    for date in stock_df.index:
        current_date = date.strftime('%Y-%m-%d')
        previous_date = stock_df.iloc[date].shift(-1).index.strftime('%Y-%m-%d')
        trades = client.list_trades(ticker, timestamp_gt=previous_date, timestamp_lte=current_date)
        average_price, total_volume, num_trades = _get_average_data_trades(trades)
        stock_df.at[date, "trade_avg_price"] = average_price
        stock_df.at[date, "trade_avg_vol"] = total_volume
        stock_df.at[date, "trade_nums"] = num_trades

    return stock_df
