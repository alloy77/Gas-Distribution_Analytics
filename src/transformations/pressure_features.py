def add_pressure_drop(df):
    df['Pressure_Drop'] = df.groupby('Meter_ID')['Pressure'].diff().fillna(0)
    return df


def add_pressure_violation(df):
    ceilings = {'domestic': 0.5, 'commercial': 4.0, 'industrial': 70.0}
    df['Pressure_Violation'] = df.apply(
        lambda r: r['Pressure'] > ceilings.get(r.get('Customer_Type', ''), 70.0),
        axis=1
    )
    return df
