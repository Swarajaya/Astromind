"""Tests for Keplerian propagator and Monte Carlo engine."""

import pytest
import numpy as np
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.physics.kepler import propagate, solve_kepler, monte_carlo, OrbitalState

APOPHIS = {
    "sma": 0.922, "ecc": 0.191, "inc": 3.3,
    "raan": 204.4, "argp": 126.4, "ma": 211.1
}
BENNU = {
    "sma": 1.126, "ecc": 0.204, "inc": 6.0,
    "raan": 2.1,  "argp": 66.2,  "ma": 101.5
}


class TestKepler:
    def test_kepler_equation_residual(self):
        """E - e*sin(E) should equal M."""
        M = np.pi / 3
        E = solve_kepler(M, 0.2)
        assert abs(E - 0.2 * np.sin(E) - M) < 1e-10

    def test_kepler_circular_orbit(self):
        """For e=0, E should equal M exactly."""
        M = 1.2
        E = solve_kepler(M, 0.0)
        assert abs(E - M) < 1e-10

    def test_propagate_returns_state(self):
        state = propagate(APOPHIS, 100)
        assert isinstance(state, OrbitalState)
        assert state.r > 0

    def test_propagate_apophis_distance(self):
        """Apophis stays in inner solar system."""
        state = propagate(APOPHIS, 365)
        assert 0.7 < state.r < 1.5, f"Unexpected r={state.r}"

    def test_propagate_bennu(self):
        state = propagate(BENNU, 0)
        assert 0.8 < state.r < 1.5

    def test_day_zero_reproducible(self):
        s1 = propagate(APOPHIS, 0)
        s2 = propagate(APOPHIS, 0)
        assert abs(s1.x - s2.x) < 1e-12

    def test_monte_carlo_runs(self):
        result = monte_carlo(APOPHIS, runs=50)
        assert "impact_probability" in result
        assert 0 <= result["impact_probability"] <= 1
        assert len(result["states"]) == 50

    def test_monte_carlo_statistics(self):
        result = monte_carlo(BENNU, runs=100)
        assert result["min_r"] > 0
        assert result["mean_r"] > result["min_r"]
        assert result["std_r"] >= 0
