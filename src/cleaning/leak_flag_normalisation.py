import pandas as pd

def normalize_leak_flag(val):
    """Maps all dirty variants to clean Yes or No."""
    yes_values = {'y', 'yes', 'Yes', 'YES', 'YEs', '1', 'TRUE', 'True', 'true'}
    no_values  = {'n', 'no', 'No', 'NO',  'nO',  '0', 'FALSE','False','false'}
    if pd.isnull(val):
        return 'Unknown'
    v = str(val).strip()
    if v in yes_values: return 'Yes'
    if v in no_values:  return 'No'
    return 'Unknown'   # catch-all for anything unexpected
