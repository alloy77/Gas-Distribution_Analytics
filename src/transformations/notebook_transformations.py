import numpy as np
import pandas as pd

# T1
def daily_aggregation(df):
    return (
        df.groupby(["Meter_ID", "DMA_Zone", "Date"])
        .agg(
            Flow_std_daily=("Flow_std", "sum"),
            Energy_daily=("Energy_calibrated", "sum"),
            Avg_Pressure=("Pressure", "mean"),
            Read_Count=("Reading_ID", "count"),
            Billable_Reads=("Is_Billable", "sum"),
        )
        .reset_index()
    )

# T3
def pressure_violation_counts(df, interval_min=15):
    violation_df = (
        df.groupby(["Meter_ID", "Customer_Type", "DMA_Zone"])
        .agg(
            Total_Readings=("Reading_ID", "count"),
            Violation_Count=("Pressure_Violation", "sum"),
            Max_Pressure=("Pressure", "max"),
            Avg_Pressure=("Pressure", "mean"),
        )
        .reset_index()
    )
    violation_df["Violation_Duration_Min"] = violation_df["Violation_Count"] * interval_min
    violation_df["Violation_Rate_%"] = (
        violation_df["Violation_Count"] / violation_df["Total_Readings"] * 100
    ).round(2)
    return violation_df

# T4
def manual_leak_propensity(df):
    df["Pressure_Drop"] = df.groupby("Meter_ID")["Pressure"].diff().fillna(0)
    df["Pressure_Drop_Flag"] = df["Pressure_Drop"] < -0.3
    df["Leak_Alarm"] = df["Leak_Flag"].map({"Yes": 1, "No": 0, "Unknown": 0}).fillna(0)
    df["Flow_Anomaly_Int"] = df.get("Flow_Outlier", pd.Series([False]*len(df))).astype(int)
    
    df["Leak_Propensity_Score"] = (
        0.5 * df["Pressure_Drop_Flag"].astype(int)
        + 0.3 * df["Flow_Anomaly_Int"]
        + 0.2 * df["Leak_Alarm"]
    ).round(3)
    df["High_Leak_Risk"] = df["Leak_Propensity_Score"] >= 0.5
    return df

# T6
def customer_consumption_profiles(df):
    customer_monthly = (
        df.groupby(["Customer_ID", "Customer_Type", "Month"])
        .agg(
            Monthly_Flow=("Flow_calibrated", "sum"),
            Monthly_Energy=("Energy_calibrated", "sum"),
        )
        .reset_index()
    )
    yearly_avg = (
        customer_monthly.groupby("Customer_ID")["Monthly_Flow"]
        .mean()
        .reset_index(name="Yearly_Avg_Flow")
    )
    customer_monthly = customer_monthly.merge(yearly_avg, on="Customer_ID")
    customer_monthly["Seasonal_Index"] = (
        customer_monthly["Monthly_Flow"] / customer_monthly["Yearly_Avg_Flow"]
    ).round(4)
    return customer_monthly

# T7
def peak_demand_detection(df):
    hourly_demand = (
        df.groupby(["Date", "Hour"])
        .agg(System_Demand=("Flow_calibrated", "sum"))
        .reset_index()
    )
    if hourly_demand.empty:
        return None, None
    peak_row = hourly_demand.loc[hourly_demand["System_Demand"].idxmax()]
    system_peak = hourly_demand["System_Demand"].max()
    
    customer_peak = (
        df.groupby("Customer_ID")["Flow_calibrated"]
        .max()
        .reset_index(name="Customer_Peak_Demand")
    )
    diversity_factor = customer_peak["Customer_Peak_Demand"].sum() / system_peak if system_peak else np.nan
    return peak_row, diversity_factor

# T9
def dma_balance(df):
    dma_input = (
        df.groupby("DMA_Zone")["Flow_std"]
        .sum()
        .reset_index(name="Gas_Input_Sm3")
    )
    dma_consumed = (
        df[df["Is_Billable"] == True]
        .groupby("DMA_Zone")["Flow_std"]
        .sum()
        .reset_index(name="Gas_Consumed_Sm3")
    )
    bal = dma_input.merge(dma_consumed, on="DMA_Zone")
    bal["DMA_Loss_Sm3"] = bal["Gas_Input_Sm3"] - bal["Gas_Consumed_Sm3"]
    bal["Loss_Percent"] = (
        bal["DMA_Loss_Sm3"] / bal["Gas_Input_Sm3"] * 100
    ).round(2)
    bal["Alert"] = bal["Loss_Percent"].apply(
        lambda x: "CRITICAL" if x > 30 else ("WARNING" if x > 20 else "OK")
    )
    return bal

# T10
def anomaly_flags(df, night_flow_threshold=20):
    df["Night_Flow_Anomaly"] = (
        (df["Hour"] >= 0)
        & (df["Hour"] <= 5)
        & (df["Flow_calibrated"] > night_flow_threshold)
    )
    df["Reverse_Flow_Flag"] = df["Direction_Flag"] == "Reverse"
    df["Flow_Anomaly_Flag"] = df["Night_Flow_Anomaly"] | df["Reverse_Flow_Flag"]
    return df

# T12
def billing_reconciliation(df):
    df["AMI_Reading"] = df["Energy_calibrated"]
    df["Billed_Reading"] = (df["AMI_Reading"] * 0.98).round(3)  # Mock implementation
    df["Billing_Gap"] = (df["AMI_Reading"] - df["Billed_Reading"]).round(3)
    
    # avoiding divide by zero with NaN
    ami_nonzero = df["AMI_Reading"].replace(0, np.nan)
    df["Billing_Discrepancy"] = (df["Billing_Gap"].abs() / ami_nonzero > 0.05).fillna(False)
    return df

# T13
def safety_kpi_mart(df):
    leak_events = df[df["Leak_Flag"] == "Yes"].copy()
    if leak_events.empty:
        return pd.DataFrame()
    np.random.seed(42)
    n = len(leak_events)
    # mock logic from notebook
    leak_events["Response_Time_Min"] = np.where(
        leak_events.get("High_Leak_Risk", False),
        np.random.randint(15, 60, n),
        np.random.randint(30, 240, n),
    )
    leak_events["Closure_Time_Min"] = np.where(
        leak_events.get("High_Leak_Risk", False),
        np.random.randint(60, 240, n),
        np.random.randint(120, 480, n),
    )
    leak_events["Response_Within_SLA"] = leak_events["Response_Time_Min"] <= 60
    leak_events["Closure_Within_SLA"] = leak_events["Closure_Time_Min"] <= 240
    
    safety_kpi = (
        leak_events.groupby("DMA_Zone")
        .agg(
            Total_Leaks=("Reading_ID", "count"),
            High_Risk_Leaks=("High_Leak_Risk", "sum") if "High_Leak_Risk" in df.columns else ("Reading_ID", "count"), # Mock sum if missing
            Avg_Response_Min=("Response_Time_Min", "mean"),
            Avg_Closure_Min=("Closure_Time_Min", "mean"),
            Response_SLA_Met=("Response_Within_SLA", "sum"),
            Closure_SLA_Met=("Closure_Within_SLA", "sum"),
        )
        .reset_index()
    )
    return safety_kpi

# T14
def gis_rollups(df):
    gis_zone = (
        df.groupby("Zone")
        .agg(
            Total_Flow_SCMH=("Flow_calibrated", "sum"),
            Avg_Pressure_bar=("Pressure", "mean"),
            Total_Energy_MMBtu=("Energy_MMBtu", "sum") if "Energy_MMBtu" in df else ("Flow_calibrated", "sum"),
            Meter_Count=("Meter_ID", "nunique"),
            Customer_Count=("Customer_ID", "nunique"),
        )
        .reset_index()
    )
    return gis_zone

# T17
def meter_health_score(df):
    meter_health = df.groupby(["Meter_ID", "Customer_Type", "DMA_Zone"]).agg(
        Stuck_Pct=("Sensor_Stuck", "mean") if "Sensor_Stuck" in df else ("Meter_ID", lambda x: 0),
        Outlier_Flow_Pct=("Flow_Outlier", "mean") if "Flow_Outlier" in df else ("Meter_ID", lambda x: 0),
        Outlier_Press_Pct=("Pressure_Outlier", "mean") if "Pressure_Outlier" in df else ("Meter_ID", lambda x: 0),
        Cal_Drift=("Cal_Coefficient", lambda x: (x - 1.0).abs().mean()) if "Cal_Coefficient" in df else ("Meter_ID", lambda x: 0),
        Capacity_Exceeded_Pct=("Capacity_Exceeded", "mean") if "Capacity_Exceeded" in df else ("Meter_ID", lambda x: 0),
        Leak_Rate=("Leak_Flag", lambda x: (x == "Yes").sum() / max(len(x), 1))
    ).reset_index()
    
    meter_health["Health_Score"] = (
        100
        - meter_health["Stuck_Pct"] * 30
        - meter_health["Outlier_Flow_Pct"] * 20
        - meter_health["Outlier_Press_Pct"] * 15
        - meter_health["Cal_Drift"] * 500
        - meter_health["Capacity_Exceeded_Pct"] * 25
        - meter_health["Leak_Rate"] * 1000
    ).clip(lower=0, upper=100)
    
    meter_health["Health_Status"] = pd.cut(
        meter_health["Health_Score"],
        bins=[-1, 40, 70, 101],
        labels=["Critical", "Maintenance Due", "Healthy"],
        right=False 
    )
    return meter_health
