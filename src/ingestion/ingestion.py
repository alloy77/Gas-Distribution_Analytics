"""High-level ingestion workflows."""
import os
from pathlib import Path
from typing import Optional

import pandas as pd

from .file_reader import read_csv


def ingest_data(
    source_path: str,
    destination_path: str,
    parse_dates: Optional[list] = None,
    dtype_map: Optional[dict] = None,
    drop_columns: Optional[list] = None,
) -> pd.DataFrame:
    """Ingest data from source_path and save a cleaned copy to destination_path."""
    df = read_csv(source_path, parse_dates=parse_dates)

    if dtype_map:
        for col, dtype in dtype_map.items():
            if col in df.columns:
                df[col] = df[col].astype(dtype)

    if drop_columns:
        to_drop = [c for c in drop_columns if c in df.columns]
        if to_drop:
            df = df.drop(columns=to_drop)

    dest = Path(destination_path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(dest, index=False)
    print(f"Ingested data saved to {destination_path}")

    return df


if __name__ == '__main__':
    # example execution path for quick manual use
    raw_path = 'data/raw/CGD_Raw.csv'
    clean_path = 'data/processed/CGD_Ingested.csv'
    print('Running ingestion from', raw_path)
    ingest_data(
        source_path=raw_path,
        destination_path=clean_path,
        parse_dates=['TS'],
        drop_columns=['Notes_Comments', 'Outage_Type'],
    )
