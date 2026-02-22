"""
neo_loader.py — Fetch and cache Near-Earth Object orbital data from NASA.

Data sources:
  1. NASA NeoWs REST API  — close approach feed by date
  2. JPL SBDB API         — orbital elements by object designation
  3. Built-in dataset     — representative sample (offline fallback)
"""

import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

NASA_API_KEY = os.getenv("NASA_API_KEY", "DEMO_KEY")
JPL_SBDB_URL = os.getenv("JPL_SBDB_URL", "https://ssd-api.jpl.nasa.gov/sbdb.api")

# ── Built-in NEO Dataset (NASA/JPL sourced) ───────────────────────────────────
# Orbital elements: J2000 epoch | Units: AU, degrees
BUILTIN_NEOS = [
    {
        "id": "2023 DW", "name": "2023 DW",
        "sma": 1.014, "ecc": 0.198, "inc": 5.0,
        "raan": 37.2, "argp": 106.1, "ma": 88.3,
        "diameter_m": 49, "pha": True, "discovery": "2023"
    },
    {
        "id": "99942", "name": "Apophis",
        "sma": 0.922, "ecc": 0.191, "inc": 3.3,
        "raan": 204.4, "argp": 126.4, "ma": 211.1,
        "diameter_m": 370, "pha": True, "discovery": "2004"
    },
    {
        "id": "101955", "name": "Bennu",
        "sma": 1.126, "ecc": 0.204, "inc": 6.0,
        "raan": 2.1, "argp": 66.2, "ma": 101.5,
        "diameter_m": 490, "pha": True, "discovery": "1999"
    },
    {
        "id": "29075", "name": "1950 DA",
        "sma": 1.699, "ecc": 0.508, "inc": 12.2,
        "raan": 356.6, "argp": 224.6, "ma": 149.2,
        "diameter_m": 1300, "pha": True, "discovery": "1950"
    },
    {
        "id": "2020 NK1", "name": "2020 NK1",
        "sma": 1.45, "ecc": 0.39, "inc": 7.8,
        "raan": 121.3, "argp": 89.5, "ma": 203.1,
        "diameter_m": 160, "pha": False, "discovery": "2020"
    },
    {
        "id": "2007 FT3", "name": "2007 FT3",
        "sma": 1.021, "ecc": 0.247, "inc": 0.9,
        "raan": 186.4, "argp": 36.9, "ma": 180.7,
        "diameter_m": 340, "pha": True, "discovery": "2007"
    },
    {
        "id": "2010 RF12", "name": "2010 RF12",
        "sma": 1.054, "ecc": 0.193, "inc": 0.8,
        "raan": 2.3, "argp": 176.1, "ma": 47.8,
        "diameter_m": 7, "pha": False, "discovery": "2010"
    },
    {
        "id": "2004 MN4", "name": "2004 MN4",
        "sma": 0.919, "ecc": 0.191, "inc": 3.3,
        "raan": 204.4, "argp": 127.4, "ma": 209.1,
        "diameter_m": 325, "pha": True, "discovery": "2004"
    },
]


def load_neo_dataframe() -> pd.DataFrame:
    """Return DataFrame of built-in NEO orbital elements."""
    return pd.DataFrame(BUILTIN_NEOS)


def fetch_from_jpl(designation: str, timeout: int = 10) -> dict:
    """
    Fetch live orbital elements from JPL Small-Body Database.

    Args:
        designation: JPL designation string (e.g. "99942", "2023 DW")
        timeout:     Request timeout in seconds

    Returns:
        dict of orbital element name → float value
    """
    resp = requests.get(
        JPL_SBDB_URL,
        params={"sstr": designation, "orb": 1, "cov": 0},
        timeout=timeout
    )
    resp.raise_for_status()
    data = resp.json()
    elements = data.get("orbit", {}).get("elements", [])
    return {el["name"]: float(el["value"]) for el in elements}


def fetch_neo_feed(start_date: str, end_date: str) -> list:
    """
    Fetch close-approach NEO feed from NASA NeoWs API.

    Args:
        start_date: YYYY-MM-DD format
        end_date:   YYYY-MM-DD format (max 7 days from start)

    Returns:
        List of dicts with id, name, pha, miss_distance_au, velocity_km_s
    """
    url    = "https://api.nasa.gov/neo/rest/v1/feed"
    params = {"start_date": start_date, "end_date": end_date, "api_key": NASA_API_KEY}
    resp   = requests.get(url, params=params, timeout=15)
    resp.raise_for_status()

    neos = []
    for date_str, objects in resp.json().get("near_earth_objects", {}).items():
        for obj in objects:
            ca = obj.get("close_approach_data", [{}])[0]
            neos.append({
                "id":               obj["id"],
                "name":             obj["name"],
                "pha":              obj["is_potentially_hazardous_asteroid"],
                "miss_distance_au": float(ca.get("miss_distance", {}).get("astronomical", 0)),
                "velocity_km_s":    float(ca.get("relative_velocity", {}).get("kilometers_per_second", 0)),
                "close_approach":   ca.get("close_approach_date", date_str),
            })
    return neos
