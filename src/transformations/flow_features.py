def add_flow_change(df):

    df["Flow_Change"] = df.groupby("Meter_ID")["Flow_calibrated"].diff().fillna(0)

    return df