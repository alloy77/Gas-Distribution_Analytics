import sys, pathlib
root = pathlib.Path(__file__).resolve().parents[2]
if str(root) not in sys.path: sys.path.insert(0, str(root))

import pandas as pd
from src.transformations.dma_assignment import assign_dma

def test_assign_dma():
    df = pd.DataFrame({'Meter_ID': ['MET-100', 'MET-140', 'BAD'], 'Latitude':[12.95, 13.2, 13.02]})
    out = assign_dma(df)
    assert out.loc[0,'DMA_Zone']=='DMA-A'
    assert out.loc[1,'DMA_Zone']=='DMA-C'
    assert out.loc[2,'DMA_Zone']=='DMA-B'
