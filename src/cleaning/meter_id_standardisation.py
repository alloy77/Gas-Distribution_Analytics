import re


def fix_meter_id(meter_id):

    mid = str(meter_id).strip().upper()

    mid = mid.replace(" ", "")

    mid = re.sub(r"-{2,}", "-", mid)

    mid = re.sub(r"^MET(\d+)$", r"MET-\1", mid)

    return mid