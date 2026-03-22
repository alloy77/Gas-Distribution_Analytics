import pytest
from src.cleaning.meter_id_standardisation import fix_meter_id

def test_fix_meter_id_standard():
    assert fix_meter_id("MET-123") == "MET-123"

def test_fix_meter_id_whitespace():
    assert fix_meter_id("  MET - 123  ") == "MET-123"

def test_fix_meter_id_lowercase():
    assert fix_meter_id("met-123") == "MET-123"

def test_fix_meter_id_double_hyphen():
    assert fix_meter_id("MET--123") == "MET-123"

def test_fix_meter_id_no_hyphen():
    assert fix_meter_id("MET123") == "MET-123"
