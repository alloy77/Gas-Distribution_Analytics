def convert_to_standard_flow(df):

    df["Flow_std"] = (
        df["Flow_calibrated"]
        * (df["Base_Pressure_kPa"] / 101.325)
        * (293.15 / (273.15 + df["Base_Temp_C"]))
    )

    return df