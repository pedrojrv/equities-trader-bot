import os
from pathlib import Path
from typing import Union

from pedrino.polygon_utils import tickers
from pedrino.data_utils import collect, saving, loading


class InvalidPedrinoDatabase(ValueError):
    pass


def setup_database(path: Union[str, Path]) -> None:
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    tickers_df = tickers.get_all(path)

    for ticker in tickers_df.ticker.values():
        data_df = collect.collect_all_to_date(ticker)
        saving.save_parquet(data_df, path)


def verify_valid_database(path: Path) -> None:
    if not path.is_dir():
        raise FileNotFoundError(f"Provided directory does not exist: {path}")
    all_stocks = path / "all_stocks.csv"
    if not all_stocks.is_file():
        raise FileNotFoundError("all_stocks.csv not found in given database directory.")
    subdirectories = [x[0] for x in os.walk(path)]
    for directory in subdirectories:
        subdir = Path(directory)
        if not subdir.stem.startswith('ticker='):
            raise InvalidPedrinoDatabase('Directory not a valid database. One or more files are contaminated.')


def update_database(path: Union[str, Path]) -> None:
    path = Path(path)
    verify_valid_database(path)
    tickers = path / "all_stocks.csv"
    for ticker in tickers:
        ticker_df = loading.load_ticker_data(ticker)
