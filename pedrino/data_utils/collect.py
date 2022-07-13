from typing import Optional
import pandas as pd
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

from pedrino.polygon_utils.aggregates import get_agg
from pedrino.polygon_utils import ticker_details, stock_financials_vx, trades
from pedrino._constants import Years, POLYGON_AGG_LIMIT


def append_extras(ticker: str, stocks_df: pd.DataFrame) -> pd.DataFrame:
    stocks_df = ticker_details.append_ticker_details(ticker, stocks_df)
    stocks_df = stock_financials_vx.append_stock_financials(ticker, stocks_df)
    stocks_df = trades.append_trades_averages(ticker, stocks_df)
    return stocks_df


def collect_minute(ticker: str, start: datetime, extras: Optional[bool] = True) -> pd.DataFrame:
    df = get_agg(ticker, start, start)
    if extras:
        df = append_extras(ticker, df)
    return df


def collect_minutes(ticker: str, start: datetime, end: datetime, extras: Optional[bool] = True) -> pd.DataFrame:
    minutes_diff = (start - end).total_seconds()
    if minutes_diff > POLYGON_AGG_LIMIT:
        raise ValueError("Cannot collect more than 50000 minutes. Request less or use other functions")
    df = get_agg(ticker, start, end)
    if extras:
        df = append_extras(ticker, df)
    return df


def collect_day(ticker: str, date: datetime, extras: Optional[bool] = True) -> pd.DataFrame:
    start = datetime(date.year, date.month, date.day)
    end = start + timedelta(days=1)
    df = get_agg(ticker, start, end)
    if extras:
        df = append_extras(ticker, df)
    return df


def collect_days(ticker: str, start: datetime, end: datetime, extras: Optional[bool] = True) -> pd.DataFrame:
    pass


def collect_month(ticker: str, date: datetime, extras: Optional[bool] = True) -> pd.DataFrame:
    start = datetime(date.year, date.month, 1)
    mock_end = start + relativedelta(month=1)
    end = datetime(date.year, mock_end.month, 1)
    df = get_agg(ticker, start, end)
    if extras:
        df = append_extras(ticker, df)
    return df


def collect_months(ticker: str, start: datetime, end: datetime, extras: Optional[bool] = True) -> pd.DataFrame:
    pass


def collect_year(ticker: str, year: int, extras: Optional[bool] = True) -> pd.DataFrame:
    start = datetime(year, 1, 1)
    yearly_data = collect_month(ticker, start, extras)
    for month in range(2, 13):
        date = datetime(year, month, 1)
        to_append = collect_month(ticker, date, extras)
        yearly_data = yearly_data.append(to_append)
    return yearly_data


def collect_years(ticker: str, years: list, extras: Optional[bool] = True) -> pd.DataFrame:
    yearly_data = collect_year(ticker, years[0], extras)
    if len(years) >= 2:
        for year in range(years[1], years[-1] + 1):
            to_append = collect_year(ticker, year, extras)
            yearly_data = yearly_data.append(to_append)
    return yearly_data


def collect_all_to_date(ticker: str, extras: Optional[bool] = True) -> pd.DataFrame:
    now = datetime.now()
    all_years = list(range(Years.STOCKS, now.year + 1))
    all_data = collect_years(ticker, all_years, extras)
    return all_data


def collect_new(ticker: str, last_date: datetime):
    now = datetime.now()
    start = datetime(last_date.year, last_date.month, last_date.date, last_date.hour, last_date.minute + 1)
    minutes_diff = (now - last_date).total_seconds() / 60
    latest_data =
    for
