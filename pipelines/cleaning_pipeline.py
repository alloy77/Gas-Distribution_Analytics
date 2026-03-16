import pandas as pd

from src.cleaning.timestamp_cleaning import fix_timestamp
from src.cleaning.meter_id_standardisation import fix_meter_id
from src.cleaning.numeric_cleaning import to_clean_number
from src.cleaning.unit_normalisation import normalize_unit
from src.cleaning.geo_parsing import split_coordinates
from src.cleaning.duplicate_removal import remove_duplicates


def run_cleaning():

    df = pd.read_csv("data/raw/CGD_Dataset_before_cleaning.csv")

    # Timestamp normalization
    df["TS"] = df["TS"].apply(fix_timestamp)

    # Meter ID cleaning
    df["Meter_ID"] = df["Meter_ID"].apply(fix_meter_id)

    # Numeric conversion
    df["Pressure"] = df["Pressure"].apply(to_clean_number)
    df["Flow"] = df["Flow"].apply(to_clean_number)
    df["Energy"] = df["Energy"].apply(to_clean_number)

    # Unit normalization
    df["Unit"] = df["Unit"].apply(normalize_unit)

    # Geo split
    df = split_coordinates(df)

    # Remove duplicates
    df = remove_duplicates(df)

    # Save cleaned dataset
    df.to_csv("data/processed/CGD_Dataset_after_cleaning.csv", index=False)

    print("Cleaning completed successfully")


if __name__ == "__main__":
    run_cleaning()