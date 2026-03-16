import sys, pathlib
root = pathlib.Path(__file__).resolve().parents[2]
if str(root) not in sys.path: sys.path.insert(0, str(root))

import pandas as pd
from src.transformations.time_features import add_time_features

def test_add_time_features():
    df = pd.DataFrame({'TS': ['2024-01-01 00:00:00', '2024-06-15 12:00:00']})
    out = add_time_features(df)
    assert out.loc[0, 'Season'] == 'Winter'
    assert out.loc[1, 'Season'] == 'Monsoon'
    assert out['Hour'].tolist() == [0, 12]
