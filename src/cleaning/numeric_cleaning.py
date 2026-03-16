import pandas as pd
import numpy as np


def to_clean_number(value):

    if pd.isnull(value):
        return np.nan

    val = str(value).strip()

    val = val.replace(",", "")

    val = val.replace("bar", "")

    try:
        return float(val)
    except:
        return np.nan