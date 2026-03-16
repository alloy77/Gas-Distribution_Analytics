import pandas as pd

def generate_ufg_results(df):
    if 'Is_Billable' not in df.columns:
        df['Is_Billable'] = True
    ufg = (
        df.groupby('DMA_Zone')
          .agg(
              Gas_Input_Sm3=('Flow_std','sum'),
              Gas_Billed_Sm3=('Flow_std', lambda x: x[df.loc[x.index,'Is_Billable'] == True].sum())
          )
          .reset_index()
    )
    ufg['UFG_Sm3'] = ufg['Gas_Input_Sm3'] - ufg['Gas_Billed_Sm3']
    ufg['UFG_Percent'] = (ufg['UFG_Sm3'] / ufg['Gas_Input_Sm3'].replace(0, pd.NA) * 100).round(2)
    return ufg

def save_ufg_results(path='data/analytics_outputs/ufg_results.csv'):
    df = pd.read_csv('data/processed/CGD_Transformation_Final.csv', parse_dates=['TS'])
    ufg = generate_ufg_results(df)
    ufg.to_csv(path, index=False)
    return ufg
