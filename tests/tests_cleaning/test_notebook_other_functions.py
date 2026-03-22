import pandas as pd
import numpy as np
import pytest
import re

from src.cleaning.outlier_detection import flag_outliers
from src.cleaning.customer_id_standardisation import standardize_customer_id, assign_customer_type
from src.cleaning.leak_flag_normalisation import normalize_leak_flag



# ------------- Pytest Cases -------------

def test_standardize_customer_id():
    assert standardize_customer_id("cid-863") == "C863"
    assert standardize_customer_id("CID-863") == "C863"
    assert standardize_customer_id(" c863 ") == "C863"
    assert standardize_customer_id("C863") == "C863"
    assert pd.isnull(standardize_customer_id(np.nan))

def test_normalize_leak_flag():
    assert normalize_leak_flag("Yes") == "Yes"
    assert normalize_leak_flag("y") == "Yes"
    assert normalize_leak_flag("1") == "Yes"
    assert normalize_leak_flag("True") == "Yes"
    
    assert normalize_leak_flag("No") == "No"
    assert normalize_leak_flag("0") == "No"
    assert normalize_leak_flag("nO") == "No"
    assert normalize_leak_flag("false") == "No"
    
    assert normalize_leak_flag("foo") == "Unknown"
    assert normalize_leak_flag(np.nan) == "Unknown"

def test_flag_outliers():
    # We need at least 10 items for the min_periods requirement
    series = pd.Series([10.0]*100)
    series.iloc[50] = 1000.0  # Huge outlier
    
    outliers = flag_outliers(series, window=50)
    assert not outliers.iloc[0]
    assert not outliers.iloc[49]
    assert outliers.iloc[50]
    assert not outliers.iloc[51]

def test_assign_customer_type():
    assert assign_customer_type("C500") == "domestic"
    assert assign_customer_type("C750") == "commercial"
    assert assign_customer_type("C900") == "industrial"
    assert assign_customer_type("unknown") == "unknown"
