import sys, pathlib
root = pathlib.Path(__file__).resolve().parents[2]
if str(root) not in sys.path: sys.path.insert(0, str(root))

import pandas as pd
from src.ml.leak_prediction import train_leak_model

def test_leak_prediction_training(tmp_path):
    df = pd.DataFrame({
        'TS': pd.date_range('2024-01-01', periods=10, freq='h'),
        'Pressure':[10,11,12,13,14,15,11,12,13,14],
        'Pressure_Drop':[0.1,0.2,0.1,0.1,0.4,0.2,0.0,0.3,0.1,0.2],
        'Flow_std':[100,110,120,90,80,130,140,130,120,110],
        'Flow_Change':[1,2,1,-1,-2,2,1,-1,1,-1],
        'DMA_Zone':['DMA-A']*10,
        'Leak_Flag':['Yes','No','No','Yes','No','No','Yes','No','No','Yes']
    })
    source=tmp_path/'input.csv'
    model=tmp_path/'model.pkl'
    df.to_csv(source,index=False)
    result=train_leak_model(str(source), str(model))
    assert model.exists()
    assert 0 <= result['accuracy'] <= 1
