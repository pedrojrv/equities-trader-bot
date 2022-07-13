import pandas as pd
from pedrino import config


def load_ticker_data(ticker: str) -> pd.DataFrame:
    database_path = config.get_database_path()
    ticker_path = database_path / f"ticker={ticker}"
    return pd.read_parquet(ticker_path)
