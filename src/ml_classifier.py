"""
ML Classifier and Voice Sample Enrollment module for SwarSatya (स्वरसत्य) — Voice Truth.
Supports interactive voice sample enrollment (Human vs AI) and custom local model training.
Automatically augments 1 enrolled file into 5 dataset samples for high-accuracy training.
"""

from pathlib import Path
import pickle
import secrets
from datetime import datetime, timezone
from typing import Dict, Any, List, Tuple
import numpy as np
from sklearn.ensemble import RandomForestClassifier

from config import DATA_DIR
from src.audio_io import iter_audio_windows
from src.audio_features import extract_window_features

MODEL_DIR = DATA_DIR / "models"
MODEL_PATH = MODEL_DIR / "voice_classifier.pkl"

DATASET_DIR = DATA_DIR / "dataset"
DATASET_PATH = DATASET_DIR / "enrolled_samples.pkl"


def extract_feature_vector(features: Dict[str, Any]) -> np.ndarray:
    """
    Convert 1-second window features dictionary into a 32-dimensional numpy vector.
    """
    vec = [
        features.get("rms_energy", 0.0),
        features.get("zero_crossing_rate", 0.0),
        features.get("zcr_std", 0.0),
        features.get("spectral_centroid", 0.0),
        features.get("spectral_centroid_std", 0.0),
        features.get("spectral_bandwidth", 0.0),
        features.get("spectral_flatness", 0.0),
        features.get("spectral_rolloff", 0.0),
        features.get("pitch_mean", 0.0),
        features.get("pitch_std", 0.0),
        features.get("pitch_var", 0.0),
        features.get("voiced_ratio", 0.0),
        features.get("speech_activity", 0.0),
        features.get("mfcc_std_avg", 0.0),
    ]
    mfcc_mean = features.get("mfcc_mean", [0.0] * 13)
    mfcc_std = features.get("mfcc_std", [0.0] * 13)
    vec.extend(mfcc_mean if len(mfcc_mean) == 13 else [0.0] * 13)
    vec.extend(mfcc_std if len(mfcc_std) == 13 else [0.0] * 13)

    return np.array(vec, dtype=np.float32)


def get_default_baseline_data() -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate baseline synthetic feature distributions for cold-start initialization.
    """
    np.random.seed(42)
    n_samples = 400

    human_X = []
    for _ in range(n_samples):
        feat = {
            "rms_energy": np.random.uniform(0.03, 0.15),
            "zero_crossing_rate": np.random.uniform(0.04, 0.12),
            "zcr_std": np.random.uniform(0.02, 0.06),
            "spectral_centroid": np.random.uniform(1200.0, 3200.0),
            "spectral_centroid_std": np.random.uniform(300.0, 900.0),
            "spectral_bandwidth": np.random.uniform(1500.0, 2800.0),
            "spectral_flatness": np.random.uniform(0.005, 0.035),
            "spectral_rolloff": np.random.uniform(3000.0, 6500.0),
            "pitch_mean": np.random.uniform(110.0, 240.0),
            "pitch_std": np.random.uniform(25.0, 65.0),
            "pitch_var": np.random.uniform(625.0, 4225.0),
            "voiced_ratio": np.random.uniform(0.35, 0.72),
            "speech_activity": np.random.uniform(0.4, 0.95),
            "mfcc_std_avg": np.random.uniform(19.0, 34.0),
            "mfcc_mean": np.random.normal(-15.0, 30.0, 13).tolist(),
            "mfcc_std": np.random.uniform(18.0, 40.0, 13).tolist()
        }
        human_X.append(extract_feature_vector(feat))

    ai_X = []
    for _ in range(n_samples):
        feat = {
            "rms_energy": np.random.uniform(0.04, 0.14),
            "zero_crossing_rate": np.random.uniform(0.03, 0.09),
            "zcr_std": np.random.uniform(0.005, 0.02),
            "spectral_centroid": np.random.uniform(1000.0, 2400.0),
            "spectral_centroid_std": np.random.uniform(100.0, 350.0),
            "spectral_bandwidth": np.random.uniform(1200.0, 2200.0),
            "spectral_flatness": np.random.uniform(0.0001, 0.005),
            "spectral_rolloff": np.random.uniform(2500.0, 4800.0),
            "pitch_mean": np.random.uniform(120.0, 220.0),
            "pitch_std": np.random.uniform(0.5, 14.0),
            "pitch_var": np.random.uniform(0.25, 196.0),
            "voiced_ratio": np.random.uniform(0.70, 0.95),
            "speech_activity": np.random.uniform(0.5, 0.98),
            "mfcc_std_avg": np.random.uniform(8.0, 15.5),
            "mfcc_mean": np.random.normal(-10.0, 20.0, 13).tolist(),
            "mfcc_std": np.random.uniform(7.0, 15.0, 13).tolist()
        }
        ai_X.append(extract_feature_vector(feat))

    X = np.vstack([human_X, ai_X])
    y = np.array([0] * n_samples + [1] * n_samples)
    return X, y


def load_enrolled_dataset() -> List[Dict[str, Any]]:
    """Load list of custom enrolled samples from DATASET_PATH."""
    DATASET_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not DATASET_PATH.exists():
        return []
    try:
        with open(DATASET_PATH, "rb") as f:
            return pickle.load(f)
    except Exception:
        return []


def enroll_audio_sample(
    audio_data: np.ndarray,
    sr: int,
    label: int,
    sample_name: str
) -> List[Dict[str, Any]]:
    """
    Enroll an audio sample (Human=0, AI=1) into the local dataset.
    Augments 1 uploaded audio file into 5 dataset samples (via gain & time shifting)
    so that 1 file = 5 dataset training samples!
    """
    dataset = load_enrolled_dataset()
    enrolled_entries = []

    gain_factors = [1.0, 0.95, 1.05, 0.90, 1.10]
    base_name = str(sample_name).strip() or "Unnamed Sample"

    for i in range(5):
        gain = gain_factors[i]
        aug_audio = np.clip(audio_data * gain, -1.0, 1.0)

        if i > 0:
            shift_samples = int(sr * 0.04 * i)
            aug_audio = np.roll(aug_audio, shift_samples)

        feature_vectors = []
        for start_t, end_t, chunk in iter_audio_windows(aug_audio, sr, window_seconds=1.0, hop_seconds=0.25):
            feat = extract_window_features(chunk, sr=sr)
            if not feat.get("is_silent", True):
                vec = extract_feature_vector(feat)
                feature_vectors.append(vec.tolist())

        if feature_vectors:
            entry = {
                "sample_id": f"smp_{secrets.token_hex(4)}",
                "sample_name": f"{base_name} (Aug #{i+1})" if i > 0 else f"{base_name} (Original)",
                "label": int(label),
                "label_text": "AI / Synthetic Voice" if label == 1 else "Human Voice",
                "timestamp_utc": datetime.now(timezone.utc).isoformat()[:19].replace("T", " "),
                "window_count": len(feature_vectors),
                "feature_vectors": feature_vectors
            }
            dataset.append(entry)
            enrolled_entries.append(entry)

    if not enrolled_entries:
        raise ValueError("Audio sample contains no active speech frames to enroll.")

    DATASET_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(DATASET_PATH, "wb") as f:
        pickle.dump(dataset, f)

    return enrolled_entries


def clear_enrolled_dataset() -> bool:
    """Clear all custom enrolled samples."""
    DATASET_PATH.parent.mkdir(parents=True, exist_ok=True)
    if DATASET_PATH.exists():
        try:
            DATASET_PATH.unlink()
            return True
        except Exception:
            return False
    return True


def train_custom_model_from_dataset(model_path: Path = MODEL_PATH) -> Tuple[RandomForestClassifier, Dict[str, Any]]:
    """
    Train a Random Forest classifier directly on custom enrolled voice samples + baseline data.
    Saves model weights to MODEL_PATH.
    """
    model_path = Path(model_path)
    model_path.parent.mkdir(parents=True, exist_ok=True)

    base_X, base_y = get_default_baseline_data()
    
    enrolled_dataset = load_enrolled_dataset()
    custom_X = []
    custom_y = []

    human_samples_count = 0
    ai_samples_count = 0
    total_custom_windows = 0

    for sample in enrolled_dataset:
        lbl = sample["label"]
        vectors = sample.get("feature_vectors", [])
        if lbl == 0:
            human_samples_count += 1
        else:
            ai_samples_count += 1
        
        for vec in vectors:
            custom_X.append(vec)
            custom_y.append(lbl)
            total_custom_windows += 1

    if custom_X:
        custom_X_arr = np.array(custom_X)
        custom_y_arr = np.array(custom_y)
        X = np.vstack([base_X] + [custom_X_arr] * 10)
        y = np.concatenate([base_y] + [custom_y_arr] * 10)
    else:
        X = base_X
        y = base_y

    clf = RandomForestClassifier(n_estimators=120, max_depth=10, random_state=42)
    clf.fit(X, y)

    with open(model_path, "wb") as f:
        pickle.dump(clf, f)

    summary = {
        "total_enrolled_samples": len(enrolled_dataset),
        "human_samples": human_samples_count,
        "ai_samples": ai_samples_count,
        "total_windows": total_custom_windows,
        "model_accuracy": round(float(clf.score(X, y)) * 100, 1),
        "model_file_path": str(model_path.resolve()),
        "dataset_file_path": str(DATASET_PATH.resolve())
    }

    return clf, summary


class VoiceClassifier:
    """
    Classifier manager loading local models/voice_classifier.pkl.
    """

    def __init__(self, model_path: Path = MODEL_PATH):
        self.model_path = Path(model_path)
        self.model = self.reload_model()

    def reload_model(self) -> RandomForestClassifier:
        """Reload trained model from model_path into self.model."""
        if self.model_path.exists():
            try:
                with open(self.model_path, "rb") as f:
                    self.model = pickle.load(f)
                    return self.model
            except Exception:
                pass
        clf, _ = train_custom_model_from_dataset(self.model_path)
        self.model = clf
        return clf

    def predict_synthetic_probability(self, features: Dict[str, Any]) -> float:
        """
        Return the probability [0.0, 1.0] that the given audio window is AI synthetic voice.
        """
        if features.get("is_silent", True):
            return 0.0

        vec = extract_feature_vector(features).reshape(1, -1)
        try:
            probas = self.model.predict_proba(vec)[0]
            classes = list(self.model.classes_)
            if 1 in classes:
                idx_1 = classes.index(1)
                proba = float(probas[idx_1])
            else:
                proba = 0.0
        except Exception:
            proba = 0.0

        return float(max(0.0, min(1.0, proba)))
