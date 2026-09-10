"""
Acoustic and prosodic feature extraction module for 1-second audio windows.
"""

from typing import Dict, Any
import numpy as np
import librosa
from config import MIN_SPEECH_RMS


def extract_window_features(
    window: np.ndarray,
    sr: int = 16000
) -> Dict[str, Any]:
    """
    Extract lightweight acoustic and prosodic features from a 1.0-second float32 audio window.
    """
    if window is None or len(window) == 0:
        return _get_empty_features()

    rms = float(np.sqrt(np.mean(window ** 2)))

    if rms < MIN_SPEECH_RMS:
        return _get_silent_features(rms)

    # 1. Zero Crossing Rate
    zcr_array = librosa.feature.zero_crossing_rate(window)
    zcr_mean = float(np.mean(zcr_array))
    zcr_std = float(np.std(zcr_array))

    # 2. Spectral Centroid & Bandwidth
    spec_cent = librosa.feature.spectral_centroid(y=window, sr=sr)
    spectral_centroid = float(np.mean(spec_cent))
    spectral_centroid_std = float(np.std(spec_cent))

    spec_bw = librosa.feature.spectral_bandwidth(y=window, sr=sr)
    spectral_bandwidth = float(np.mean(spec_bw))

    # 3. Spectral Flatness & Rolloff
    spec_flat = librosa.feature.spectral_flatness(y=window)
    spectral_flatness = float(np.mean(spec_flat))

    spec_roll = librosa.feature.spectral_rolloff(y=window, sr=sr)
    spectral_rolloff = float(np.mean(spec_roll))

    # 4. MFCC Features (13 coefficients)
    mfcc = librosa.feature.mfcc(y=window, sr=sr, n_mfcc=13)
    mfcc_mean = np.mean(mfcc, axis=1).tolist()
    mfcc_std = np.std(mfcc, axis=1).tolist()
    mfcc_std_avg = float(np.mean(mfcc_std))

    # 5. Pitch Estimation via YIN over broader pitch range (50 Hz to 600 Hz)
    f0_mean = 0.0
    f0_std = 0.0
    f0_var = 0.0
    voiced_ratio = 0.0

    try:
        f0 = librosa.yin(window, fmin=50, fmax=600, sr=sr)
        valid_f0 = f0[(f0 > 50) & (f0 < 550)]

        if len(valid_f0) > 0:
            f0_mean = float(np.mean(valid_f0))
            f0_std = float(np.std(valid_f0))
            f0_var = float(np.var(valid_f0))
            voiced_ratio = float(len(valid_f0)) / float(len(f0))
    except Exception:
        f0_mean = 0.0
        f0_std = 0.0
        f0_var = 0.0
        voiced_ratio = 0.0

    speech_activity = float(min(1.0, rms / 0.08))

    return {
        "is_silent": False,
        "rms_energy": round(rms, 5),
        "zero_crossing_rate": round(zcr_mean, 5),
        "zcr_std": round(zcr_std, 5),
        "spectral_centroid": round(spectral_centroid, 2),
        "spectral_centroid_std": round(spectral_centroid_std, 2),
        "spectral_bandwidth": round(spectral_bandwidth, 2),
        "spectral_flatness": round(spectral_flatness, 6),
        "spectral_rolloff": round(spectral_rolloff, 2),
        "mfcc_mean": [round(x, 4) for x in mfcc_mean],
        "mfcc_std": [round(x, 4) for x in mfcc_std],
        "mfcc_std_avg": round(mfcc_std_avg, 4),
        "pitch_mean": round(f0_mean, 2),
        "pitch_std": round(f0_std, 2),
        "pitch_var": round(f0_var, 2),
        "voiced_ratio": round(voiced_ratio, 4),
        "speech_activity": round(speech_activity, 4),
    }


def _get_silent_features(rms: float) -> Dict[str, Any]:
    return {
        "is_silent": True,
        "rms_energy": round(rms, 5),
        "zero_crossing_rate": 0.0,
        "zcr_std": 0.0,
        "spectral_centroid": 0.0,
        "spectral_centroid_std": 0.0,
        "spectral_bandwidth": 0.0,
        "spectral_flatness": 0.0,
        "spectral_rolloff": 0.0,
        "mfcc_mean": [0.0] * 13,
        "mfcc_std": [0.0] * 13,
        "mfcc_std_avg": 0.0,
        "pitch_mean": 0.0,
        "pitch_std": 0.0,
        "pitch_var": 0.0,
        "voiced_ratio": 0.0,
        "speech_activity": 0.0,
    }


def _get_empty_features() -> Dict[str, Any]:
    return _get_silent_features(0.0)
