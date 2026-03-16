def detect_stuck_sensors(df):

    df["Flow_Variance"] = df.groupby("Meter_ID")["Flow"].transform("var")

    df["Sensor_Stuck"] = df["Flow_Variance"] == 0

    return df