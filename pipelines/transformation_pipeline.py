import pandas as pd

from src.transformations.calibration import apply_calibration
from src.transformations.standard_conditions import convert_to_standard_flow
from src.transformations.time_features import add_time_features
from src.transformations.flow_features import add_flow_change
from src.transformations.pressure_features import add_pressure_drop, add_pressure_violation
from src.transformations.dma_assignment import assign_dma
from src.transformations.gps_normalization import normalize_gps
from src.transformations.outage_classification import classify_outage
from src.transformations.revenue_assurance import compute_revenue_flags
from src.transformations.ufg_analysis import calculate_ufg
from src.transformations.carbon import calculate_carbon


def run_transformation():
    df = pd.read_csv('data/processed/CGD_Dataset_after_cleaning.csv')

    df['TS'] = pd.to_datetime(df['TS'], errors='coerce')
    df = apply_calibration(df)
    df = convert_to_standard_flow(df)
    df = add_time_features(df)
    df = normalize_gps(df)
    df = assign_dma(df)

    # Fill missing calibrated values from adjacent readings per meter
    for col in ['Flow_calibrated', 'Energy_calibrated', 'Flow_std']:
        if col in df.columns:
            df[col] = df.groupby('Meter_ID')[col].ffill().bfill()

    # Add meter-status features
    df = add_flow_change(df)
    df = add_pressure_drop(df)
    df = add_pressure_violation(df)
    df = classify_outage(df)
    df = compute_revenue_flags(df)
    df = calculate_carbon(df)

    # Zone categorization used by notebooks
    if 'Latitude' in df.columns:
        df['Zone'] = pd.cut(df['Latitude'], bins=[-1, 12.9, 13.1, 90],
                            labels=['Zone_A', 'Zone_B', 'Zone_C'])

    # Unaccounted-for Gas summary for reference
    ufg_df = calculate_ufg(df)

    # Save transformed dataset and derived reports
    df.to_csv('data/processed/transformed_dataset.csv', index=False)
    ufg_df.to_csv('data/processed/ufg_dataset.csv', index=False)

    print('Transformation complete')
    print('Transformed rows:', len(df))
    print('UFG zones:', len(ufg_df))


if __name__ == '__main__':
    run_transformation()
