"""Utility to append ticker financial details to an aggregate dataframe."""
import logging
import numpy as np
from collections import OrderedDict

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


def _create_financial_columns(stock_df):
    for col in ALL_FINANCIAL_COLS:
        stock_df[col] = np.nan
    return stock_df


def _append_balance_sheet_info(stock_df, date, balance_sheet_info):
    # balance sheet info
    for key in BALANCE_SHEET_KEYS.keys():
        stock_df.at[date, BALANCE_SHEET_KEYS[key]] = balance_sheet_info[key].value
    return stock_df


def _append_cash_flow_info(stock_df, date, cash_flow_info):
    # cash flow info
    for key in CASH_FLOW_KEYS.keys():
        value = getattr(cash_flow_info, key)
        to_append = value if value is not None else np.nan
        stock_df.at[date, CASH_FLOW_KEYS[key]] = to_append
    return stock_df


def _append_comprehensive_income_info(stock_df, date, comprehensive_income_info):
    # comprehensive income
    for key in COMPREHENSIVE_INCOME_KEYS.keys():
        sub_object = getattr(comprehensive_income_info, key)
        value = sub_object.value
        to_append = value if value is not None else np.nan
        stock_df.at[date, COMPREHENSIVE_INCOME_KEYS[key]] = to_append
    return stock_df


def _append_income_statement_info(stock_df, date, income_statement_info):
    # income statement
    for key in INCOME_STATEMENT_KEYS.keys():
        sub_object = getattr(income_statement_info, key)
        value = sub_object.value
        to_append = value if value is not None else np.nan
        stock_df.at[date, INCOME_STATEMENT_KEYS[key]] = to_append
    return stock_df


def append_stock_financials(client, ticker, stock_df):
    """Append stock financials to a dataframe.

    Parameters
    ----------
    client : polygon.RESTClient
        Client authorized to make financial requests.
    ticker : str
        Company's ticker symbol.
    stock_df : pandas.DataFrame
        DataFrame to append information to.

    Returns
    -------
    pandas.DataFrame
        The modified dataframe with financials appended to it.
    """
    stock_df = _create_financial_columns(stock_df)

    for date in stock_df.index:
        datetime = date.strftime('%Y-%m-%d')
        financials = client.vx.list_stock_financials(ticker, filing_date=datetime)
        stock_financials = next(financials, False)
        if not stock_financials:
            continue

        if date.year != getattr(stock_financials, 'fiscal_year'):
            logger.warning("Data does not match fiscal year. Skipping.")
            continue

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
