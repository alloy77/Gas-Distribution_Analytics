import numpy as np
import pytest
from src.cleaning.numeric_cleaning import to_clean_number

def test_to_clean_number_standard():
    assert to_clean_number("123.45") == 123.45

def test_to_clean_number_comma():
    assert to_clean_number("1,157") == 1157.0

def test_to_clean_number_bar():
    assert to_clean_number("1.5bar") == 1.5

def test_to_clean_number_spaces():
    assert to_clean_number(" 123.45 ") == 123.45

def test_to_clean_number_integer():
    assert to_clean_number(100) == 100.0

def test_to_clean_number_null():
    assert np.isnan(to_clean_number(np.nan))

def test_to_clean_number_invalid():
    assert np.isnan(to_clean_number("invalid"))
