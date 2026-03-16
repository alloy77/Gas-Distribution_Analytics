import sys, pathlib
root = pathlib.Path(__file__).resolve().parents[2]
if str(root) not in sys.path: sys.path.insert(0, str(root))

import pandas as pd
from src.cleaning.timestamp_cleaning import fix_timestamp

def test_date_parsing():
    val = '2024-01-01 00:00:00'
    dt = fix_timestamp(val)
    assert str(dt).startswith('2024-01-01')
