import pandas as pd


def compute_revenue_flags(df):
    if 'Sensor_Reliable' not in df.columns:
        df['Sensor_Reliable'] = False
    if 'Maintenance_Flag' not in df.columns:
        df['Maintenance_Flag'] = None
    if 'Flow_calibrated' not in df.columns:
        df['Flow_calibrated'] = pd.NA

    df['Read_Success'] = (
        (df['Sensor_Reliable'] == True) &
        (df['Maintenance_Flag'] == 'NORMAL') &
        (df['Flow_calibrated'].notna())
    )
    df['Estimated_Read'] = ~df['Read_Success']
    return df
