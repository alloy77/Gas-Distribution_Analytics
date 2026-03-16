def normalize_unit(unit):

    unit_map = {
        "SCMH": "SCMH",
        "scmh": "SCMH",
        "Scmh": "SCMH",
        "SCM/H": "SCMH",
        "scm/h": "SCMH",
        "Sm^3/h": "SCMH",
        "sm^3/h": "SCMH",
        "Sm3/h": "SCMH",
        "m3/h": "SCMH",
        "S m^3/h": "SCMH",
    }

    unit = str(unit).strip()

    return unit_map.get(unit, "SCMH")