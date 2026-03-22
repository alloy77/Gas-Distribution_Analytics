import pandas as pd
import numpy as np
import pytest
from src.cleaning.geo_parsing import split_coordinates

def test_split_coordinates():
    df = pd.DataFrame({"Latitude,Longitude": ["13.0324,80.1744", " 12.9747 , 80.2142  ", "invalid"]})
    df_clean = split_coordinates(df)
    
    assert "Latitude" in df_clean.columns
    assert "Longitude" in df_clean.columns
    assert "Latitude,Longitude" not in df_clean.columns
    
    assert df_clean["Latitude"].iloc[0] == 13.0324
    assert df_clean["Longitude"].iloc[0] == 80.1744
    
    assert df_clean["Latitude"].iloc[1] == 12.9747
    assert df_clean["Longitude"].iloc[1] == 80.2142
    
    assert np.isnan(df_clean["Latitude"].iloc[2])
    assert np.isnan(df_clean["Longitude"].iloc[2])

def test_split_coordinates_with_parens():
    df = pd.DataFrame({"Latitude,Longitude": ["(13.0, 80.1)"]})
    df_clean = split_coordinates(df)
    
    assert df_clean["Latitude"].iloc[0] == 13.0
    assert df_clean["Longitude"].iloc[0] == 80.1
