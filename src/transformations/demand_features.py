def demand_features(df):

    df["Daily_Demand"] = df.groupby("Date")["Flow_std"].transform("sum")

    df["Rolling_Demand"] = df["Daily_Demand"].rolling(7).mean()

    return df