import numpy as np

def normalize_gps(df):
    if 'Latitude' in df.columns and 'Longitude' in df.columns and 'Meter_ID' in df.columns:
        df['Latitude'] = df.groupby('Meter_ID')['Latitude'].transform(
            lambda x: x.mode()[0] if x.notna().any() else np.nan
        )
        df['Longitude'] = df.groupby('Meter_ID')['Longitude'].transform(
            lambda x: x.mode()[0] if x.notna().any() else np.nan
        )
    return df
