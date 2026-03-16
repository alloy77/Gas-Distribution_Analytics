import sys, pathlib
root = pathlib.Path(__file__).resolve().parents[2]
if str(root) not in sys.path: sys.path.insert(0, str(root))

import pandas as pd
from src.transformations.ufg_analysis import calculate_ufg

def test_calculate_ufg():
    df = pd.DataFrame({
        'DMA_Zone': ['DMA-A','DMA-A'],
        'Flow_std': [100, 50],
        'Is_Billable': [True, False],
    })
    out = calculate_ufg(df)
    assert out.loc[0, 'UFG_Percent'] == 33.33
