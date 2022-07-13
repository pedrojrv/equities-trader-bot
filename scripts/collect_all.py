from pathlib import Path

from pedrino import Years
from pedrino import collect
from pedrino.polygon_utils import tickers


def main():
    tickers_df = tickers.get_all()
    all_tickers = list(tickers_df.ticker.values)
