"""Basic file-reading utilities for ingestion."""
import pandas as pd
from pathlib import Path
from typing import Optional


def read_csv(file_path: str, parse_dates: Optional[list] = None) -> pd.DataFrame:
    """Read a CSV file from a path and return DataFrame."""
    p = Path(file_path)
    if not p.exists():
        raise FileNotFoundError(f"CSV file not found: {file_path}")

    df = pd.read_csv(p, parse_dates=parse_dates)
    print(f"Loaded {len(df)} rows from {file_path}")
    return df


def read_parquet(file_path: str) -> pd.DataFrame:
    """Read a Parquet file from a path and return DataFrame."""
    p = Path(file_path)
    if not p.exists():
        raise FileNotFoundError(f"Parquet file not found: {file_path}")

    df = pd.read_parquet(p)
    print(f"Loaded {len(df)} rows from {file_path}")
    return df
