import pandas as pd
from datetime import timedelta


def fix_timestamp(ts_str):

    ts_str = str(ts_str).strip()

    # Fix 24:xx timestamps
    if "24:" in ts_str:
        ts_str = ts_str.replace("24:", "00:")
        dt = pd.to_datetime(ts_str, errors="coerce")
        if pd.notnull(dt):
            dt = dt + timedelta(days=1)
        return dt

    # Remove Z timezone
    if ts_str.endswith("Z"):
        ts_str = ts_str.replace("Z", "")

    return pd.to_datetime(ts_str, errors="coerce")