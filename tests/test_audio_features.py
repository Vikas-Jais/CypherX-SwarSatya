"""
Unit tests for 32-dimensional acoustic feature extraction module (src/audio_features.py).
"""

import sys
from pathlib import Path
import numpy as np
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.audio_features import extract_window_features


def test_extract_window_features_shapes():
    """Verify that extract_window_features returns all expected dictionary keys and values."""
    sr = 16000
    # Generate 1 second of 440 Hz sine wave
    t = np.linspace(0, 1.0, sr, endpoint=False)
    y = (0.5 * np.sin(2 * np.pi * 440 * t)).astype(np.float32)

    features = extract_window_features(y, sr=sr)
    assert isinstance(features, dict)
    assert features["is_silent"] is False
    assert "rms_energy" in features
    assert "pitch_mean" in features
    assert "spectral_flatness" in features
    assert len(features["mfcc_mean"]) == 13
    assert len(features["mfcc_std"]) == 13


def test_silent_signal_extraction():
    """Verify silence handling in feature extraction."""
    sr = 16000
    y_silent = np.zeros(sr, dtype=np.float32)

    features = extract_window_features(y_silent, sr=sr)
    assert features["is_silent"] is True
    assert features["rms_energy"] == 0.0
