import pandas as pd
from pathlib import Path


def save_parquet(df: pd.DataFrame, path: Path) -> None:
    df.to_parquet(path, partition_cols=['ticker'])
