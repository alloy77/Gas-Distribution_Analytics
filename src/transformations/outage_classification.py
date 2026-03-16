def classify_outage(df):
    df['Is_Billable'] = df['Maintenance_Flag'].isnull()
    df['outage_flag'] = (
        (df['Flow'] == 0) |
        (df['Pressure'] < 5) |
        (df['Leak_Flag'] == 'Yes') |
        (df['Maintenance_Flag'].isin(['MAINTENANCE', 'SHUTDOWN']))
    ).astype(int)

    df['prev_flag'] = df.groupby('Meter_ID')['outage_flag'].shift(1).fillna(0)
    df['event_type'] = None
    df.loc[(df['outage_flag'] == 1) & (df['prev_flag'] == 0), 'event_type'] = 'OUTAGE_START'
    df.loc[(df['outage_flag'] == 0) & (df['prev_flag'] == 1), 'event_type'] = 'OUTAGE_END'

    return df
