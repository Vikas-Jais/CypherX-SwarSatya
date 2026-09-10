"""
Unit tests for audio input/output and signal processing module (src/audio_io.py).
"""

import sys
from pathlib import Path
import numpy as np
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.audio_io import (
    generate_synthetic_demo_signal,
    iter_audio_windows,
    load_audio,
    get_audio_metadata
)


def test_generate_synthetic_demo_signal():
    """Verify synthetic demo signals generated for robotic synthetic vs natural speech modes."""
    y_robotic, sr_r = generate_synthetic_demo_signal(duration_seconds=1.0, sr=16000, mode="robotic_synthetic")
    assert sr_r == 16000
    assert len(y_robotic) == 16000
    assert y_robotic.dtype == np.float32

    y_natural, sr_n = generate_synthetic_demo_signal(duration_seconds=1.0, sr=16000, mode="natural_human")
    assert sr_n == 16000
    assert len(y_natural) == 16000
    assert y_natural.dtype == np.float32


def test_iter_audio_windows():
    """Verify sliding window generator yielding start, end, chunk."""
    sr = 16000
    y = np.ones(sr * 3, dtype=np.float32)  # 3 seconds audio
    windows = list(iter_audio_windows(y, sr=sr, window_seconds=1.0, hop_seconds=0.25))

    # Expect 9 full windows + 1 padded trailing window = 10 total windows
    assert len(windows) >= 9
    for start_t, end_t, chunk in windows:
        assert len(chunk) == sr
        assert end_t > start_t


def test_get_audio_metadata():
    """Verify metadata calculation for audio array."""
    sr = 16000
    y = (0.5 * np.ones(sr * 2)).astype(np.float32)
    meta = get_audio_metadata(y, sr)
    assert meta["duration_seconds"] == 2.0
    assert meta["sample_rate"] == 16000
    assert meta["channels"] == 1
