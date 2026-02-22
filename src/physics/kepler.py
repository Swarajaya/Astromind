"""
kepler.py — Keplerian orbital propagator.

Solves Kepler's equation M = E - e·sin(E) via Newton-Raphson,
then converts eccentric anomaly → true anomaly → Cartesian ECI.

Reference: Bate, Mueller & White — Fundamentals of Astrodynamics (1971)
"""

import numpy as np
from dataclasses import dataclass, field
from typing import List


@dataclass
class OrbitalState:
    x:   float   # Heliocentric X (AU)
    y:   float   # Heliocentric Y (AU)
    z:   float   # Heliocentric Z (AU)
    r:   float   # Radial distance from Sun (AU)
    nu:  float   # True anomaly (degrees)
    day: float   # Epoch offset (days)


def solve_kepler(M_rad: float, ecc: float,
                 tol: float = 1e-12, max_iter: int = 50) -> float:
    """
    Newton-Raphson solver for Kepler's transcendental equation.

    Args:
        M_rad:    Mean anomaly in radians
        ecc:      Orbital eccentricity [0, 1)
        tol:      Convergence tolerance
        max_iter: Maximum iterations

    Returns:
        Eccentric anomaly E in radians
    """
    E = M_rad + ecc * np.sin(M_rad)  # Better initial guess (Encke)
    for _ in range(max_iter):
        f  =  E - ecc * np.sin(E) - M_rad
        fp =  1 - ecc * np.cos(E)
        dE = -f / fp
        E += dE
        if abs(dE) < tol:
            break
    return E


def propagate(params: dict, days: float) -> OrbitalState:
    """
    Propagate Keplerian orbit forward by `days` from epoch.

    Coordinate system: Heliocentric ECI (J2000)

    Args:
        params: dict with keys:
                  sma  — semi-major axis (AU)
                  ecc  — eccentricity [0, 1)
                  inc  — inclination (degrees)
                  raan — right ascension of ascending node (degrees)
                  argp — argument of periapsis (degrees)
                  ma   — mean anomaly at epoch (degrees)
        days:   Propagation time in days

    Returns:
        OrbitalState with heliocentric Cartesian position
    """
    sma  = float(params["sma"])
    ecc  = float(params["ecc"])
    inc  = np.radians(float(params["inc"]))
    raan = np.radians(float(params["raan"]))
    argp = np.radians(float(params["argp"]))

    # Mean motion: n = sqrt(GM/a³) — for AU & days: n = 0.9856076686 deg/day / a^1.5
    n = np.radians(0.9856076686 / sma ** 1.5)
    M = np.radians(float(params["ma"])) + n * days
    M = M % (2 * np.pi)

    E  = solve_kepler(M, ecc)
    nu = 2 * np.arctan2(
        np.sqrt(1 + ecc) * np.sin(E / 2),
        np.sqrt(1 - ecc) * np.cos(E / 2)
    )
    r = sma * (1 - ecc * np.cos(E))

    # Rotation matrices: perifocal → geocentric ECI
    cos_raan = np.cos(raan);  sin_raan = np.sin(raan)
    cos_inc  = np.cos(inc);   sin_inc  = np.sin(inc)
    cos_w    = np.cos(argp + nu); sin_w = np.sin(argp + nu)

    x = r * (cos_raan * cos_w - sin_raan * sin_w * cos_inc)
    y = r * (sin_raan * cos_w + cos_raan * sin_w * cos_inc)
    z = r * (sin_w * sin_inc)

    return OrbitalState(x=x, y=y, z=z, r=r, nu=np.degrees(nu), day=days)


def monte_carlo(params: dict, runs: int = 1000, days: float = 365.0,
                sigma_sma: float = 0.02, sigma_ecc: float = 0.01,
                sigma_ang: float = 1.0) -> dict:
    """
    Monte Carlo uncertainty propagation over Keplerian orbital elements.

    Adds Gaussian noise to each element per its observational uncertainty,
    propagates forward, and counts Earth-crossing events.

    Args:
        params:     Nominal orbital element dict
        runs:       Number of random samples
        days:       Propagation horizon in days
        sigma_sma:  Fractional 1-sigma uncertainty on semi-major axis
        sigma_ecc:  Absolute 1-sigma uncertainty on eccentricity
        sigma_ang:  Absolute 1-sigma uncertainty on angular elements (degrees)

    Returns:
        dict:
          impact_probability: float — fraction of runs that cross Earth's orbit
          states:             List[OrbitalState]
          min_r, mean_r, std_r: radial statistics
          runs:               int
    """
    rng    = np.random.default_rng(seed=42)
    states: List[OrbitalState] = []
    impacts = 0

    for _ in range(runs):
        noisy = {
            "sma":  params["sma"] * (1 + rng.normal(0, sigma_sma)),
            "ecc":  float(np.clip(params["ecc"] + rng.normal(0, sigma_ecc), 0, 0.999)),
            "inc":  params["inc"]  + rng.normal(0, sigma_ang),
            "raan": params["raan"] + rng.normal(0, sigma_ang),
            "argp": params["argp"] + rng.normal(0, sigma_ang),
            "ma":   params["ma"]   + rng.normal(0, sigma_ang * 2),
        }
        state = propagate(noisy, days)
        states.append(state)

        # Earth-crossing: Earth orbits at ~1 AU; threshold < 0.05 AU (≈7.5M km)
        if abs(state.r - 1.0) < 0.05:
            impacts += 1

    radii = np.array([s.r for s in states])
    return {
        "impact_probability": impacts / runs,
        "states":             states,
        "runs":               runs,
        "min_r":              float(radii.min()),
        "mean_r":             float(radii.mean()),
        "std_r":              float(radii.std()),
    }
