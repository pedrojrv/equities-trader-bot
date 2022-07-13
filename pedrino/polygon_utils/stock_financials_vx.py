"""Utility to append ticker financial details to an aggregate dataframe."""
import logging
import numpy as np
import pandas as pd

from typing import Dict, Union
from collections import OrderedDict

from polygon.rest.models.financials import DataPoint, CashFlowStatement, ComprehensiveIncome, IncomeStatement
from pedrino import client

logger = logging.getLogger(__file__)

BALANCE_SHEET_KEYS = OrderedDict({
    'liabilities_and_equity': 'liabilities_and_equity',
    'current_assets': 'curr_assets',
    'assets': 'assets',
    'equity_attributable_to_parent': 'equity_parent',
    'fixed_assets': 'fixed_assets',
    'noncurrent_liabilities': 'noncurr_liabilities',
    'other_than_fixed_noncurrent_assets': 'otfnc_assets',
    'current_liabilities': 'curr_liabilities',
    'equity': 'equity',
    'equity_attributable_to_noncontrolling_interest': 'noncontrolling_equity',
    'noncurrent_assets': 'noncurr_assets',
    'liabilities': 'libabilities',
})

CASH_FLOW_KEYS = OrderedDict({
    'exchange_gains_losses': 'gain_losses',
    'net_cash_flow': 'net_cash_flow',
    'net_cash_flow_from_financing_activities': 'NCF_finacial_activities',
})

COMPREHENSIVE_INCOME_KEYS = OrderedDict({
    'comprehensive_income_loss': 'CIL',
    'comprehensive_income_loss_attributable_to_parent': 'parent_CIL',
    'other_comprehensive_income_loss': 'other_CIL',
})

INCOME_STATEMENT_KEYS = OrderedDict({
    'basic_earnings_per_share': 'EPS',
    'cost_of_revenue': 'cost_of_revenue',
    'gross_profit': 'gross_profit',
    'operating_expenses': 'op_expenses',
    'revenues': 'revenues',
})


ALL_FINANCIAL_COLS = list(BALANCE_SHEET_KEYS.values()) + list(CASH_FLOW_KEYS.values()) + \
    list(COMPREHENSIVE_INCOME_KEYS.values()) + list(INCOME_STATEMENT_KEYS.values())


def _create_financial_columns(stock_df: pd.DataFrame) -> pd.DataFrame:
    """Create empty columns for each financial feature."""
    for col in ALL_FINANCIAL_COLS:
        stock_df[col] = np.nan
    return stock_df


def _append_balance_sheet_info(
        stock_df: pd.DataFrame, date: str, balance_sheet_info: Dict[str, DataPoint]) -> pd.DataFrame:
    """Append balance sheet information.

    Parameters
    ----------
    stock_df : pd.DataFrame
        Dataframe on which to append balance sheet information. The date must be available as an index.
    date : str
        Date index on the dataframe.
    balance_sheet_info : Dict[str, DataPoint]
        Balance sheet response from the polygon client `.list_stock_financials()`.

    Returns
    -------
    pd.DataFrame
        DataFrame with the appended balance sheet information.
    """
    for key in BALANCE_SHEET_KEYS.keys():
        stock_df.at[date, BALANCE_SHEET_KEYS[key]] = balance_sheet_info[key].value
    return stock_df


def _process_and_append_financial_info(
        df: pd.DataFrame, date: str, column_mapping: Dict[str, str],
        financial_object: Union[CashFlowStatement, ComprehensiveIncome, IncomeStatement]) -> pd.DataFrame:
    """Append generic financial data object to dataframe."""
    for key in column_mapping.keys():
        sub_object = getattr(financial_object, key)
        to_append = sub_object.value if sub_object is not None else np.nan
        df.at[date, column_mapping[key]] = to_append
    return df


def _append_cash_flow_info(stock_df: pd.DataFrame, date: str, cash_flow_info: CashFlowStatement) -> pd.DataFrame:
    """Append the cash flow information from the polygon response to the dataframe."""
    return _process_and_append_financial_info(stock_df, date, CASH_FLOW_KEYS, cash_flow_info)


def _append_comprehensive_income_info(
        stock_df: pd.DataFrame, date: str, comprehensive_income_info: ComprehensiveIncome) -> pd.DataFrame:
    """Append the comprehensive income information from the polygon response to the dataframe."""
    return _process_and_append_financial_info(stock_df, date, COMPREHENSIVE_INCOME_KEYS, comprehensive_income_info)


def _append_income_statement_info(
        stock_df: pd.DataFrame, date: str, income_statement_info: IncomeStatement) -> pd.DataFrame:
    """Append the income statement information from the polygon response to the dataframe."""
    return _process_and_append_financial_info(stock_df, date, INCOME_STATEMENT_KEYS, income_statement_info)


def append_stock_financials(ticker: str, stock_df: pd.DataFrame) -> pd.DataFrame:
    """Append stock financials to a dataframe.

    Parameters
    ----------
    ticker : str
        Company's ticker symbol.
    stock_df : pandas.DataFrame
        DataFrame to append information to.

    Returns
    -------
    pandas.DataFrame
        The modified dataframe with financials appended to it.
    """
    cl = client.get_client()
    stock_df = _create_financial_columns(stock_df)

    for date in stock_df.index:
        datetime = date.strftime('%Y-%m-%d')
        financials = cl.vx.list_stock_financials(ticker, filing_date=datetime)
        stock_financials = next(financials, False)
        if not stock_financials:
            continue

        if date.year != getattr(stock_financials, 'fiscal_year'):
            logger.warning("Data does not match fiscal year. Skipping.")

        stock_df.at[date, 'fiscal_period'] = getattr(stock_financials, 'fiscal_period')
        balance_sheet_info = stock_financials.financials.balance_sheet
        stock_df = _append_balance_sheet_info(stock_df, date, balance_sheet_info)

        cash_flow_info = stock_financials.financials.cash_flow_statement
        stock_df = _append_cash_flow_info(stock_df, date, cash_flow_info)

        comprehensive_income_info = stock_financials.financials.comprehensive_income
        stock_df = _append_comprehensive_income_info(stock_df, date, comprehensive_income_info)

        income_statement_info = stock_financials.financials.income_statement
        stock_df = _append_income_statement_info(stock_df, date, income_statement_info)
    return stock_df
