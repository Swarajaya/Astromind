"""Tests for Quantum VQC and ML Ensemble modules."""

import numpy as np
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.quantum.vqc import amplitude_encode, vqc_predict
from src.ml.ensemble import extract_features, gbm_predict, hybrid_predict


BENNU  = {"sma": 1.126, "ecc": 0.204, "inc": 6.0, "raan": 2.1,  "argp": 66.2,  "ma": 101.5}
APOPHIS = {"sma": 0.922, "ecc": 0.191, "inc": 3.3, "raan": 204.4, "argp": 126.4, "ma": 211.1}


# ── VQC Tests ────────────────────────────────────────────────────────────────

class TestVQC:
    def test_amplitude_encode_shape(self):
        v = amplitude_encode(BENNU)
        assert v.shape == (8,)

    def test_amplitude_encode_normalized(self):
        v = amplitude_encode(BENNU)
        assert abs(np.linalg.norm(v) - 1.0) < 1e-9

    def test_amplitude_encode_deterministic(self):
        v1 = amplitude_encode(BENNU)
        v2 = amplitude_encode(BENNU)
        np.testing.assert_array_equal(v1, v2)

    def test_vqc_predict_returns_float(self):
        score = vqc_predict(BENNU)
        assert isinstance(score, float)

    def test_vqc_predict_nonnegative(self):
        for params in [BENNU, APOPHIS]:
            score = vqc_predict(params)
            assert score >= 0, f"Negative score: {score}"

    def test_vqc_predict_deterministic(self):
        s1 = vqc_predict(BENNU)
        s2 = vqc_predict(BENNU)
        assert abs(s1 - s2) < 1e-12


# ── Ensemble Tests ───────────────────────────────────────────────────────────

class TestEnsemble:
    def test_feature_extraction_shape(self):
        f = extract_features(BENNU)
        assert f.shape == (12,)

    def test_feature_extraction_finite(self):
        f = extract_features(APOPHIS)
        assert np.all(np.isfinite(f))

    def test_gbm_predict_range(self):
        f = extract_features(BENNU)
        p = gbm_predict(f)
        assert 0 <= p <= 1, f"Out of range: {p}"

    def test_hybrid_predict_keys(self):
        result = hybrid_predict(BENNU, qml_score=0.15, mc_prob=0.002)
        expected_keys = {"qml_score", "gbm_probability", "mc_probability",
                         "hybrid_probability", "risk_level"}
        assert expected_keys.issubset(result.keys())

    def test_hybrid_predict_probability_range(self):
        result = hybrid_predict(APOPHIS, qml_score=0.3, mc_prob=0.01)
        assert 0 <= result["hybrid_probability"] <= 1

    def test_hybrid_predict_risk_label(self):
        result = hybrid_predict(BENNU, qml_score=0.05, mc_prob=0.001)
        assert result["risk_level"] in ["MINIMAL", "LOW", "ELEVATED", "CRITICAL"]

    def test_high_risk_label(self):
        result = hybrid_predict(BENNU, qml_score=0.9, mc_prob=0.9)
        assert result["risk_level"] == "CRITICAL"

    def test_low_risk_label(self):
        result = hybrid_predict(BENNU, qml_score=0.001, mc_prob=0.0001)
        assert result["risk_level"] == "MINIMAL"
