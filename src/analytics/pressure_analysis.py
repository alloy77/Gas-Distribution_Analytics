import pandas as pd

def generate_pressure_violations(df):
    if 'Pressure_Violation' not in df.columns:
        df['Pressure_Violation'] = False
    pv = (
        df.groupby(['Meter_ID','DMA_Zone'])
          .agg(
              Violation_Count=('Pressure_Violation','sum'),
              Avg_Pressure=('Pressure','mean'),
              Max_Pressure=('Pressure','max'),
              Read_Count=('Reading_ID','count')
          )
          .reset_index()
    )
    return pv

def save_pressure_violations(path='data/analytics_outputs/pressure_violations.csv'):
    df = pd.read_csv('data/processed/CGD_Transformation_Final.csv')
    pv = generate_pressure_violations(df)
    pv.to_csv(path, index=False)
    return pv
