import pandas as pd


def add_time_features(df):
    if not pd.api.types.is_datetime64_any_dtype(df['TS']):
        df['TS'] = pd.to_datetime(df['TS'], errors='coerce')

    df['Hour']   = df['TS'].dt.hour
    df['Date']   = df['TS'].dt.date
    df['Month']  = df['TS'].dt.month
    df['Hour_bucket'] = df['TS'].dt.floor('h')

    season_map = {
        12: 'Winter', 1: 'Winter', 2: 'Winter',
        3: 'Summer', 4: 'Summer', 5: 'Summer',
        6: 'Monsoon', 7: 'Monsoon', 8: 'Monsoon',
        9: 'PostMonsoon', 10: 'PostMonsoon', 11: 'PostMonsoon'
    }
    df['Season'] = df['Month'].map(season_map)
    return df
