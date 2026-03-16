import sys, pathlib
root = pathlib.Path(__file__).resolve().parents[2]
if str(root) not in sys.path: sys.path.insert(0, str(root))

import pandas as pd
from src.ml.demand_forecast import generate_30d_demand_forecast

def test_demand_forecast_generation(tmp_path):
    df = pd.DataFrame({'TS': pd.date_range('2024-01-01', periods=90, freq='D'), 'Flow_std': range(90)})
    source=tmp_path/'input.csv'
    out=tmp_path/'forecast.csv'
    df.to_csv(source,index=False)
    result=generate_30d_demand_forecast(str(source), str(out))
    assert len(result)==30
    assert out.exists()
