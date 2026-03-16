def apply_calibration(df):

    df["Flow_calibrated"] = df["Flow"] * df["Cal_Coefficient"]

    df["Energy_calibrated"] = df["Energy"] * df["Cal_Coefficient"]

    return df