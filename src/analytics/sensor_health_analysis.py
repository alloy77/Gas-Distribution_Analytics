import pandas as pd

def generate_sensor_health(df):
    if 'Sensor_Stuck' not in df.columns:
        df['Sensor_Stuck'] = False
    sh = (
        df.groupby('Meter_ID')
          .agg(
              Flow_Variance=('Flow_calibrated','var'),
              Sensor_Stuck_Count=('Sensor_Stuck','sum'),
              Read_Count=('Reading_ID','count')
          )
          .reset_index()
    )
    sh['Sensor_Stuck_Pct'] = (sh['Sensor_Stuck_Count'] / sh['Read_Count'] * 100).round(2)
    return sh

def save_sensor_health(path='data/analytics_outputs/sensor_health.csv'):
    df = pd.read_csv('data/processed/CGD_Transformation_Final.csv')
    sh = generate_sensor_health(df)
    sh.to_csv(path, index=False)
    return sh
