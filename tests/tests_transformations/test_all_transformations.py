import pytest
import pandas as pd
import numpy as np
from src.transformations.aggregation import hourly_aggregation
from src.transformations.calibration import apply_calibration
from src.transformations.carbon import calculate_carbon
from src.transformations.dma_assignment import assign_dma
from src.transformations.outage_classification import classify_outage
from src.transformations.pressure_features import add_pressure_violation
from src.transformations.notebook_transformations import (
    daily_aggregation, pressure_violation_counts, manual_leak_propensity,
    customer_consumption_profiles, peak_demand_detection, dma_balance,
    anomaly_flags, billing_reconciliation,
    meter_health_score
)

def test_hourly_aggregation():
    df = pd.DataFrame({
        "Meter_ID": ["M1", "M1"],
        "DMA_Zone": ["DMA-A", "DMA-A"],
        "Hour_bucket": [pd.to_datetime("2024-01-01 10:00:00")] * 2,
        "Flow_std": [10.0, 20.0],
        "Energy_calibrated": [1.0, 2.0],
        "Pressure": [5.0, 5.0],
        "Reading_ID": ["R1", "R2"],
        "Is_Billable": [True, False],
    })
    res = hourly_aggregation(df)
    assert len(res) == 1
    assert res["Flow_std_hourly"].iloc[0] == 30.0
    assert res["Billable_Reads"].iloc[0] == 1

def test_apply_calibration():
    df = pd.DataFrame({"Flow": [100.0], "Energy": [2.0], "Cal_Coefficient": [1.05]})
    res = apply_calibration(df)
    assert np.isclose(res["Flow_calibrated"].iloc[0], 105.0)

def test_calculate_carbon():
    df = pd.DataFrame({"Flow_calibrated": [1055.056 / 38.0]}) # should yield 1 MMBtu
    res = calculate_carbon(df)
    assert np.isclose(res["Energy_MMBtu"].iloc[0], 1.0)
    assert np.isclose(res["CO2_kg"].iloc[0], 53.07)

def test_assign_dma():
    df = pd.DataFrame({"Meter_ID": ["MET-110", "MET-125", "MET-135", "MET-150"]})
    res = assign_dma(df)
    assert res["DMA_Zone"].iloc[0] == "DMA-A"
    assert res["DMA_Zone"].iloc[1] == "DMA-B"
    assert res["DMA_Zone"].iloc[2] == "DMA-C"
    assert res["DMA_Zone"].iloc[3] == "DMA-D"

def test_classify_outage():
    df = pd.DataFrame({
        "Meter_ID": ["M1", "M1"],
        "Flow": [10.0, 0.0],
        "Pressure": [10.0, 4.0],
        "Leak_Flag": ["No", "Yes"],
        "Maintenance_Flag": [None, "MAINTENANCE"]
    })
    res = classify_outage(df)
    assert res["outage_flag"].iloc[0] == 0
    assert res["outage_flag"].iloc[1] == 1
    assert res["event_type"].iloc[1] == "OUTAGE_START"

def test_add_pressure_violation():
    df = pd.DataFrame({
        "Pressure": [0.6, 5.0, 80.0, 0.4],
        "Customer_Type": ["domestic", "commercial", "industrial", "domestic"]
    })
    res = add_pressure_violation(df)
    assert res["Pressure_Violation"].tolist() == [True, True, True, False]

def test_daily_aggregation():
    df = pd.DataFrame({
        "Meter_ID": ["M1", "M1"],
        "DMA_Zone": ["DMA-A", "DMA-A"],
        "Date": [pd.to_datetime("2024-01-01").date()] * 2,
        "Flow_std": [100.0, 50.0],
        "Energy_calibrated": [2.0, 1.0],
        "Pressure": [5.0, 6.0],
        "Reading_ID": [1, 2],
        "Is_Billable": [True, True]
    })
    res = daily_aggregation(df)
    assert len(res) == 1
    assert res["Flow_std_daily"].iloc[0] == 150.0

def test_pressure_violation_counts():
    df = pd.DataFrame({
        "Meter_ID": ["M1", "M1"],
        "Customer_Type": ["domestic", "domestic"],
        "DMA_Zone": ["DMA-A", "DMA-A"],
        "Reading_ID": [1, 2],
        "Pressure_Violation": [True, False],
        "Pressure": [0.6, 0.4]
    })
    res = pressure_violation_counts(df)
    assert len(res) == 1
    assert res["Violation_Count"].iloc[0] == 1
    assert res["Violation_Duration_Min"].iloc[0] == 15

def test_manual_leak_propensity():
    df = pd.DataFrame({
        "Meter_ID": ["M1", "M1"],
        "Pressure": [5.0, 4.5],  # Drop of -0.5 (True flag)
        "Leak_Flag": ["No", "Yes"], # 0, 1
        "Flow_Outlier": [False, True]
    })
    res = manual_leak_propensity(df)
    # The second row: drop flag int: 1. Outlier int: 1. Leak int: 1. sum = 0.5+0.3+0.2 = 1.0 > 0.5 true
    assert res["High_Leak_Risk"].iloc[1] == True

def test_customer_consumption_profiles():
    df = pd.DataFrame({
        "Customer_ID": ["C1", "C1"],
        "Customer_Type": ["domestic", "domestic"],
        "Month": [1, 2],
        "Flow_calibrated": [100.0, 200.0],
        "Energy_calibrated": [10.0, 20.0]
    })
    res = customer_consumption_profiles(df)
    assert len(res) == 2
    # Yearly avg flow = 150. Month 1 flow = 100. Seasonal index = 100/150 = 0.6667
    assert np.isclose(res["Seasonal_Index"].iloc[0], 0.6667, atol=1e-3)

def test_peak_demand_detection():
    df = pd.DataFrame({
        "Date": [pd.to_datetime("2024-01-01").date()] * 2,
        "Hour": [1, 2],
        "Flow_calibrated": [100.0, 500.0],
        "Customer_ID": ["C1", "C1"]
    })
    peak_row, diversity = peak_demand_detection(df)
    assert peak_row["Hour"] == 2
    assert diversity == 1.0

def test_dma_balance():
    df = pd.DataFrame({
        "DMA_Zone": ["DMA-A", "DMA-A"],
        "Flow_std": [100.0, 80.0], # Input conceptually
        "Is_Billable": [True, False] # 80 is not billable! 
    })
    # the function sums ALL Flow_std for Input, and Is_Billable for Consumed.
    # Total Input = 180. Consumed = 100. Loss = 80. 80/180 = ~44.4%
    res = dma_balance(df)
    assert res["Loss_Percent"].iloc[0] == 44.44
    assert res["Alert"].iloc[0] == "CRITICAL"

def test_anomaly_flags():
    df = pd.DataFrame({
        "Hour": [2, 10], # 2 is night, 10 is day
        "Flow_calibrated": [30.0, 30.0], # night threshold is 20
        "Direction_Flag": ["Forward", "Reverse"]
    })
    res = anomaly_flags(df)
    assert res["Flow_Anomaly_Flag"].tolist() == [True, True] # Night anomaly first, Reverse flow second

def test_billing_reconciliation():
    df = pd.DataFrame({
        "Energy_calibrated": [100.0, 0.0]
    })
    res = billing_reconciliation(df)
    assert len(res) == 2

def test_meter_health_score():
    df = pd.DataFrame({
        "Meter_ID": ["M1"],
        "Customer_Type": ["domestic"],
        "DMA_Zone": ["DMA-A"],
        "Sensor_Stuck": [True],   # Penalty -30
        "Flow_Outlier": [True],   # Penalty -20
        "Pressure_Outlier": [False],
        "Cal_Coefficient": [1.0],
        "Capacity_Exceeded": [False],
        "Leak_Flag": ["No"]       # Leak Rate 0
    })
    # Initial 100 - 30 - 20 = 50. Output Health_Score = 50.
    res = meter_health_score(df)
    assert np.isclose(res["Health_Score"].iloc[0], 50)
    assert res["Health_Status"].iloc[0] == "Maintenance Due"
