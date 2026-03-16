import pandas as pd

def generate_hourly_demand(df):
    hourly = (
        df.groupby(['Meter_ID','DMA_Zone','Hour_bucket'])
          .agg(
              Flow_std_hourly=('Flow_std','sum'),
              Energy_hourly=('Energy_calibrated','sum'),
              Avg_Pressure=('Pressure','mean'),
              Read_Count=('Reading_ID','count')
          )
          .reset_index()
    )
    return hourly

def save_hourly_demand(path='data/analytics_outputs/hourly_demand.csv'):
    df = pd.read_csv('data/processed/CGD_Transformation_Final.csv', parse_dates=['TS','Hour_bucket'])
    hourly = generate_hourly_demand(df)
    hourly.to_csv(path, index=False)
    return hourly
