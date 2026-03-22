import pandas as pd
import numpy as np
import re

def standardize_customer_id(cid):
    if pd.isnull(cid):
        return np.nan

    cid = str(cid).strip().upper()       # strip spaces, uppercase

    # 'CID-726' -> 'C726'  (remove the 'ID-' part, keep digits)
    match = re.match(r'^CID-(\d+)$', cid)
    if match:
        return 'C' + match.group(1)

    return cid                           # already clean e.g. 'C726'

def assign_customer_type(cid):
    try:
        num = int(re.search(r'\d+', str(cid)).group())
        if num <= 740:
            return 'domestic'
        elif num <= 860:
            return 'commercial'
        else:
            return 'industrial'
    except Exception:
        return 'unknown'
