import pandas as pd

def calculate_ufg(df):
    gas_input = df.groupby('DMA_Zone')['Flow_std'].sum().reset_index(name='Gas_Input_Sm3')
    gas_billed = df[df['Is_Billable'] == True].groupby('DMA_Zone')['Flow_std'].sum().reset_index(name='Gas_Billed_Sm3')
    ufg = gas_input.merge(gas_billed, on='DMA_Zone', how='left').fillna(0)
    ufg['UFG_Sm3'] = ufg['Gas_Input_Sm3'] - ufg['Gas_Billed_Sm3']
    ufg['UFG_Percent'] = (ufg['UFG_Sm3'] / ufg['Gas_Input_Sm3'].replace(0, pd.NA) * 100).round(2)
    return ufg
