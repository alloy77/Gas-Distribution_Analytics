import pandas as pd

def generate_zone_consumption(df):
    zone = (
        df.groupby(['DMA_Zone','Zone'])
          .agg(
              Flow_std=('Flow_std','sum'),
              Energy=('Energy_calibrated','sum'),
              Avg_Pressure=('Pressure','mean'),
              Read_Count=('Reading_ID','count')
          )
          .reset_index()
    )
    return zone

def save_zone_consumption(path='data/analytics_outputs/zone_consumption.csv'):
    df = pd.read_csv('data/processed/CGD_Transformation_Final.csv', parse_dates=['TS'])
    zone = generate_zone_consumption(df)
    zone.to_csv(path, index=False)
    return zone
