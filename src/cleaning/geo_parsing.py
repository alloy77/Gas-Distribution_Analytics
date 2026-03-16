import pandas as pd


def split_coordinates(df):

    coords = df["Latitude,Longitude"].astype(str)

    coords = coords.str.replace("(", "")
    coords = coords.str.replace(")", "")

    lat_lon = coords.str.split(",", expand=True)

    df["Latitude"] = pd.to_numeric(lat_lon[0].str.strip(), errors="coerce")
    df["Longitude"] = pd.to_numeric(lat_lon[1].str.strip(), errors="coerce")

    df.drop(columns=["Latitude,Longitude"], inplace=True)

    return df