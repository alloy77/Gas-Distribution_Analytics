def hourly_aggregation(df):

    hourly_df = (
        df.groupby(["Meter_ID", "DMA_Zone", "Hour_bucket"])
        .agg(
            Flow_std_hourly=("Flow_std", "sum"),
            Energy_hourly=("Energy_calibrated", "sum"),
            Avg_Pressure=("Pressure", "mean"),
            Read_Count=("Reading_ID", "count"),
            Billable_Reads=("Is_Billable", "sum"),
        )
        .reset_index()
    )

    return hourly_df