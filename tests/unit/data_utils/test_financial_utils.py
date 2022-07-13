import pandas as pd
from polygon.rest.models.financials import DataPoint, CashFlowStatement, ComprehensiveIncome, IncomeStatement

from pedrino.polygon_utils import stock_financials_vx


def test_create_financial_columns():
    df = pd.DataFrame()
    df = stock_financials_vx._create_financial_columns(df)
    for column in stock_financials_vx.ALL_FINANCIAL_COLS:
        assert column in df.columns


def test_append_balance_sheet_info():
    date = "2022-01-01"
    df = pd.DataFrame({'date': [date]}).set_index('date')
    df = stock_financials_vx._create_financial_columns(df)

    def _get_mock_datapoint(value):
        return DataPoint.from_dict({'value': value})

    mock_datapoint = {key: _get_mock_datapoint(100.55) for key, _ in stock_financials_vx.BALANCE_SHEET_KEYS.items()}

    stock_financials_vx._append_balance_sheet_info(df, date, mock_datapoint)
    for col in stock_financials_vx.BALANCE_SHEET_KEYS.values():
        assert col in df.columns
        assert df.loc[date, col] == 100.55


def test_append_cash_flow_info():
    date = "2022-01-01"
    df = pd.DataFrame({'date': [date]}).set_index('date')
    df = stock_financials_vx._create_financial_columns(df)

    mock_datapoint = CashFlowStatement.from_dict({
        'exchange_gains_losses': {'value': 100.55},
        'net_cash_flow': {'value': 200.55},
        'net_cash_flow_from_financing_activities': {'value': 50.55},
    })

    df = stock_financials_vx._append_cash_flow_info(df, date, mock_datapoint)
    for col, value in zip(stock_financials_vx.CASH_FLOW_KEYS.values(), [100.55, 200.55, 50.55]):
        assert col in df.columns
        assert df.loc[date, col] == value


def test_append_comprehensive_income_info():
    date = "2022-01-01"
    df = pd.DataFrame({'date': [date]}).set_index('date')
    df = stock_financials_vx._create_financial_columns(df)

    mock_datapoint = ComprehensiveIncome.from_dict({
        'comprehensive_income_loss': {'value': 100.55},
        'comprehensive_income_loss_attributable_to_parent': {'value': 200.55},
        'other_comprehensive_income_loss': {'value': 50.55},
    })

    df = stock_financials_vx._append_comprehensive_income_info(df, date, mock_datapoint)
    for col, value in zip(stock_financials_vx.COMPREHENSIVE_INCOME_KEYS.values(), [100.55, 200.55, 50.55]):
        assert col in df.columns
        assert df.loc[date, col] == value


def test_append_income_statement_info():
    date = "2022-01-01"
    df = pd.DataFrame({'date': [date]}).set_index('date')
    df = stock_financials_vx._create_financial_columns(df)

    mock_datapoint = IncomeStatement.from_dict({
        'basic_earnings_per_share': {'value': 100.55},
        'cost_of_revenue': {'value': 200.55},
        'gross_profit': {'value': 50.55},
        'operating_expenses': {'value': 100.55},
        'revenues': {'value': 200.55},
    })

    df = stock_financials_vx._append_income_statement_info(df, date, mock_datapoint)
    for col, value in zip(stock_financials_vx.INCOME_STATEMENT_KEYS.values(), [100.55, 200.55, 50.55, 100.55, 200.55]):
        assert col in df.columns
        assert df.loc[date, col] == value


def test_append_stock_financials():
    ticker = "NVDA"
    date = "2022-05-27"
    df = pd.DataFrame({'date': [date]}).set_index('date')
    df.index = pd.to_datetime(df.index)
    df = stock_financials_vx.append_stock_financials(ticker, df)

    assert df.isna().sum().sum() == 1
    assert df.fiscal_period[0] == 'Q1'
    assert len(df) == 1
