def remove_duplicates(df):

    df = df.sort_values("TS")

    df = df.drop_duplicates(
        subset=["Meter_ID", "TS"],
        keep="last"
    )

    return df