import pandas as pd
import numpy as np

def flag_outliers(series, window=50):
    """
    For each value, look at a rolling window of specified length surrounding readings.
    If the value falls outside Q1 - 1.5*IQR or Q3 + 1.5*IQR, it is an outlier.
    min_periods=10 means we need at least 10 values in the window to calculate.
    """
    q1  = series.rolling(window, min_periods=10, center=True).quantile(0.25)
    q3  = series.rolling(window, min_periods=10, center=True).quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    return (series < lower) | (series > upper)
