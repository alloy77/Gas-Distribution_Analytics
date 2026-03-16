import numpy as np


def assign_dma(df):
    def _zone_from_meter_id(meter_id):
        try:
            n = int(str(meter_id).split('-')[-1])
        except Exception:
            return 'DMA-UNKNOWN'
        if n <= 115:
            return 'DMA-A'
        if n <= 130:
            return 'DMA-B'
        if n <= 145:
            return 'DMA-C'
        return 'DMA-D'

    df['DMA_Zone'] = df['Meter_ID'].apply(_zone_from_meter_id)

    # fallback if Latitude-based assignment is needed
    if 'Latitude' in df.columns:
        mask = df['DMA_Zone'] == 'DMA-UNKNOWN'
        conditions = [
            df['Latitude'] < 12.9,
            df['Latitude'].between(12.9, 13.05),
            df['Latitude'].between(13.05, 13.15),
            df['Latitude'] > 13.15,
        ]
        zones = ['DMA-A', 'DMA-B', 'DMA-C', 'DMA-D']
        df.loc[mask, 'DMA_Zone'] = np.select(conditions, zones, default='DMA-UNKNOWN')[mask]

    return df
