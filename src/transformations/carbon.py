def calculate_carbon(df):
    CO2_KG_PER_MMBTU = 53.07
    CO2_KG_PER_TN = 1000.0

    df['Energy_MMBtu'] = (df['Flow_calibrated'] * 38.0 / 1055.056).round(4)
    df['CO2_kg'] = (df['Energy_MMBtu'] * CO2_KG_PER_MMBTU).round(3)
    df['CO2_Tonnes'] = (df['CO2_kg'] / CO2_KG_PER_TN).round(6)
    return df
