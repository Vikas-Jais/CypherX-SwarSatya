"""
Unit tests for PrototypeRiskEngine class with ML model integration.
"""

import sys
from pathlib import Path
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.risk_engine import PrototypeRiskEngine


def test_score_bounds():
    """Verify raw scores and EMA scores remain strictly within [0.0, 1.0]."""
    engine = PrototypeRiskEngine(ema_alpha=0.35)

    features = {
        "is_silent": False,
        "voiced_ratio": 0.5,
        "pitch_mean": 150.0,
        "pitch_std": 35.0,
        "spectral_flatness": 0.02,
        "spectral_centroid": 2000.0,
        "mfcc_mean": [-15.0] * 13,
        "mfcc_std": [25.0] * 13,
        "mfcc_std_avg": 25.0,
        "speech_activity": 0.8
    }

    res = engine.score_window(features)
    assert 0.0 <= res["raw_score"] <= 1.0

    ema_score = engine.update_ema(res["raw_score"])
    assert 0.0 <= ema_score <= 1.0


def test_classification_thresholds():
    """Verify SAFE, WARNING, and CRITICAL thresholds."""
    engine = PrototypeRiskEngine()

    assert engine.classify(0.10) == "SAFE"
    assert engine.classify(0.49) == "SAFE"
    assert engine.classify(0.50) == "WARNING"
    assert engine.classify(0.69) == "WARNING"
    assert engine.classify(0.70) == "CRITICAL"
    assert engine.classify(0.99) == "CRITICAL"


def test_silent_audio_handling():
    """Verify that silent windows return raw_score=0.0 and skipped=True."""
    engine = PrototypeRiskEngine()

    features = {
        "is_silent": True,
        "rms_energy": 0.001,
        "speech_activity": 0.0
    }

    res = engine.score_window(features)
    assert res["raw_score"] == 0.0
    assert res["skipped"] is True
    assert "skipped" in res["contributions"][0].lower()


def test_ema_smoothing():
    """Verify Exponential Moving Average (EMA) calculation."""
    alpha = 0.35
    engine = PrototypeRiskEngine(ema_alpha=alpha)

    score1 = 0.20
    score2 = 0.80

    ema1 = engine.update_ema(score1)
    assert ema1 == score1

    expected_ema2 = round((alpha * score2) + ((1 - alpha) * ema1), 4)
    ema2 = engine.update_ema(score2)
    assert abs(ema2 - expected_ema2) < 1e-4
