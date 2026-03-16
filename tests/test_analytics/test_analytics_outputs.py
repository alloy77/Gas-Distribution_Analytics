import sys, pathlib
root = pathlib.Path(__file__).resolve().parents[2]
if str(root) not in sys.path: sys.path.insert(0, str(root))

import pandas as pd
from src.analytics import generate_hourly_demand, generate_ufg_results, generate_pressure_violations, generate_leak_statistics


def test_analytics_modules_importable():
    assert callable(generate_hourly_demand)
    assert callable(generate_ufg_results)
    assert callable(generate_pressure_violations)
    assert callable(generate_leak_statistics)
