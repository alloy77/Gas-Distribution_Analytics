import pytest
from src.cleaning.unit_normalisation import normalize_unit

def test_normalize_unit_standard():
    assert normalize_unit("SCMH") == "SCMH"

def test_normalize_unit_lowercase():
    assert normalize_unit("scmh") == "SCMH"

def test_normalize_unit_other_variants():
    assert normalize_unit("S m^3/h") == "SCMH"
    assert normalize_unit("SCM/H") == "SCMH"
    assert normalize_unit("Sm3/h") == "SCMH"
    assert normalize_unit("m3/h") == "SCMH"

def test_normalize_unit_unknown():
    assert normalize_unit("UNKNOWN") == "SCMH"
