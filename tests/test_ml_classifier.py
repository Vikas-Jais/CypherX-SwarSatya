"""
Unit tests for local ML Scikit-Learn Classifier and 1-to-5 dataset augmentation (src/ml_classifier.py).
"""

import sys
from pathlib import Path
import numpy as np
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.ml_classifier import (
    VoiceClassifier,
    enroll_audio_sample,
    train_custom_model_from_dataset,
    extract_feature_vector
)


def test_enrollment_and_1_to_5_augmentation(tmp_path):
    """Enroll 1 Human sample and 1 AI sample, verify 1 file = 5 dataset samples augmentation, model training, and predictions."""
    import src.ml_classifier as ml_mod
    
    data_dir = tmp_path / "data"
    dataset_file = data_dir / "dataset" / "enrolled_samples.pkl"
    model_file = data_dir / "models" / "voice_classifier.pkl"

    # Patch paths temporarily for test
    orig_dataset_path = ml_mod.DATASET_PATH
    orig_model_path = ml_mod.MODEL_PATH
    ml_mod.DATASET_PATH = dataset_file
    ml_mod.MODEL_PATH = model_file

    try:
        sr = 16000
        # 1-second sine waves with speech modulation
        t = np.linspace(0, 1.0, sr, endpoint=False)
        y_human = (0.5 * np.sin(2 * np.pi * 200 * t)).astype(np.float32)
        y_ai = (0.5 * np.sin(2 * np.pi * 800 * t)).astype(np.float32)

        # Enroll human sample -> should add 5 augmented entries into dataset
        entries_h = enroll_audio_sample(y_human, sr, label=0, sample_name="test_human")
        assert len(entries_h) == 5

        # Enroll AI sample -> should add 5 augmented entries into dataset
        entries_a = enroll_audio_sample(y_ai, sr, label=1, sample_name="test_ai")
        assert len(entries_a) == 5

        # Train Random Forest model on enrolled dataset
        clf, summary = train_custom_model_from_dataset(model_path=model_file)
        assert summary["total_enrolled_samples"] == 10
        assert summary["human_samples"] == 5
        assert summary["ai_samples"] == 5
        assert model_file.exists()

        # Load trained classifier and test prediction
        classifier = VoiceClassifier(model_path=model_file)
        from src.audio_features import extract_window_features
        feat = extract_window_features(y_human, sr=sr)
        proba = classifier.predict_synthetic_probability(feat)
        assert 0.0 <= proba <= 1.0

    finally:
        ml_mod.DATASET_PATH = orig_dataset_path
        ml_mod.MODEL_PATH = orig_model_path
