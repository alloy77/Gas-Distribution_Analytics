import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression


def generate_30d_demand_forecast(data_path='data/processed/CGD_Transformation_Final.csv', output_path='data/analytics_outputs/demand_forecast_30d.csv'):
    df = pd.read_csv(data_path, parse_dates=['TS'])
    if 'Flow_std' not in df.columns:
        raise ValueError('Flow_std required in input data')

    daily = (
        df.set_index('TS')
          .resample('D')['Flow_std']
          .sum()
          .reset_index()
          .rename(columns={'TS':'ds','Flow_std':'y'})
    )

    daily = daily.dropna().reset_index(drop=True)
    daily['t'] = np.arange(len(daily))
    model = LinearRegression()
    model.fit(daily[['t']], daily['y'])
    future_t = np.arange(len(daily), len(daily)+30)
    yhat = model.predict(future_t.reshape(-1, 1))

    out = pd.DataFrame({
        'ds': pd.date_range(daily['ds'].max() + pd.Timedelta(days=1), periods=30, freq='D'),
        'yhat': yhat,
        'yhat_lower': yhat * 0.95,
        'yhat_upper': yhat * 1.05,
    })

    out.to_csv(output_path, index=False)
    return out
