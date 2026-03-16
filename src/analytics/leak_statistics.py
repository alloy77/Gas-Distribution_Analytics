import pandas as pd

def generate_leak_statistics(df):
    if 'Leak_Flag' not in df.columns:
        df['Leak_Flag'] = 'No'
    if 'High_Leak_Risk' not in df.columns:
        df['High_Leak_Risk'] = False
    if 'Leak_Score' not in df.columns:
        df['Leak_Score'] = 0.0
    leak = (
        df.groupby('Meter_ID')
          .agg(
              Leak_Events=('Leak_Flag', lambda x: (x == 'Yes').sum()),
              High_Leak_Risk=('High_Leak_Risk','sum'),
              Avg_Leak_Score=('Leak_Score','mean'),
              Read_Count=('Reading_ID','count')
          )
          .reset_index()
    )
    leak['Leak_Rate_Percent'] = (leak['Leak_Events'] / leak['Read_Count'] * 100).round(2)
    return leak

def save_leak_statistics(path='data/analytics_outputs/leak_statistics.csv'):
    df = pd.read_csv('data/processed/CGD_Transformation_Final.csv')
    leak = generate_leak_statistics(df)
    leak.to_csv(path, index=False)
    return leak
