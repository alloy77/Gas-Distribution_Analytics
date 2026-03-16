def leak_propensity_features(df):

    df["Leak_Score"] = (
        abs(df["Pressure_Drop"]) +
        abs(df["Flow_Change"])
    )

    return df