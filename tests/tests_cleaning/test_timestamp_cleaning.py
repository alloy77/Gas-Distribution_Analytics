import pandas as pd
import pytest
from datetime import timedelta
import numpy as np
from src.cleaning.timestamp_cleaning import fix_timestamp

def test_fix_timestamp_standard():
    dt = fix_timestamp("2024-04-10 14:30")
    # depending on parsing, it will match datetime
    assert dt == pd.to_datetime("2024-04-10 14:30")

def test_fix_timestamp_24_rollover():
    dt = fix_timestamp("2024-04-10 24:00")
    expected = pd.to_datetime("2024-04-11 00:00:00")
    assert dt == expected

def test_fix_timestamp_z_timezone():
    dt = fix_timestamp("2024-04-10T14:30:00Z")
    assert dt == pd.to_datetime("2024-04-10 14:30:00")

def test_fix_timestamp_invalid():
    dt = fix_timestamp("invalid-date")
    assert pd.isnull(dt)

def test_fix_timestamp_empty():
    dt = fix_timestamp("")
    assert pd.isnull(dt)
