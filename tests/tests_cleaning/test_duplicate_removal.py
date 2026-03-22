import pandas as pd
import pytest
from src.cleaning.duplicate_removal import remove_duplicates

def test_remove_duplicates():
    df = pd.DataFrame({
        "Meter_ID": ["MET-1", "MET-1", "MET-2", "MET-1"],
        "TS": [
            pd.to_datetime("2024-01-01 10:00"),
            pd.to_datetime("2024-01-01 10:00"),
            pd.to_datetime("2024-01-01 10:00"),
            pd.to_datetime("2024-01-01 11:00")
        ],
        "Value": [1, 2, 3, 4]
    })
    
    df_clean = remove_duplicates(df)
    
    assert len(df_clean) == 3
    
    # MET-1 at 10:00 should keep the last value
    met1_1000 = df_clean[(df_clean["Meter_ID"] == "MET-1") & (df_clean["TS"] == pd.to_datetime("2024-01-01 10:00"))]
    assert len(met1_1000) == 1
    assert met1_1000["Value"].iloc[0] == 2
