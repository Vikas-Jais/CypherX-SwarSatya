"""
Explainable ML-powered risk engine for prototype synthetic voice detection.
Uses Scikit-Learn Random Forest Classifier (local ML model) combined with
acoustic feature attribution for robust Human vs AI Voice detection.
"""

from typing import Dict, Any, List, Optional
import numpy as np
from config import (
    THRESHOLD_SAFE,
    THRESHOLD_WARNING,
    EMA_ALPHA,
    BASE_HEURISTIC_SCORE
)
from src.ml_classifier import VoiceClassifier


class PrototypeRiskEngine:
    """
    ML-Powered Synthetic Voice Risk Engine.
    Uses local Scikit-Learn Random Forest model (exportable to ONNX/TFLite for mobile).
    """

    def __init__(self, ema_alpha: float = EMA_ALPHA):
        self.ema_alpha = ema_alpha
        self.ema_score: float = 0.0
        self.window_count: int = 0
        self.classifier = VoiceClassifier()

    def reset(self) -> None:
        """Reset internal EMA state for a new session/audio scan."""
        self.ema_score = 0.0
        self.window_count = 0

    def score_window(
        self,
        features: Dict[str, Any],
        prev_features: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Evaluate a single 1-second window dictionary using local ML model + feature attributions.

        Returns:
            Dict containing:
            - raw_score: float [0.0, 1.0]
            - contributions: List[str] explanation of triggering heuristics/ML predictions
            - skipped: bool (True if silence/skipped)
        """
        if features.get("is_silent", True):
            return {
                "raw_score": 0.0,
                "contributions": ["No active speech / skipped"],
                "skipped": True
            }

        # 1. Predict Synthetic AI Probability via ML Model [0.0, 1.0]
        ml_prob = self.classifier.predict_synthetic_probability(features)
        contributions: List[str] = []

        if ml_prob >= 0.50:
            contributions.append(f"ML Model: High synthetic AI voice probability ({ml_prob*100:.1f}%).")
        else:
            contributions.append(f"ML Model: Natural human voice profile ({(1.0 - ml_prob)*100:.1f}% human confidence).")

        # 2. Acoustic Feature Attributions for Explainability
        pitch_std = features.get("pitch_std", 0.0)
        voiced_ratio = features.get("voiced_ratio", 0.0)
        mfcc_std_avg = features.get("mfcc_std_avg", 20.0)
        spectral_flatness = features.get("spectral_flatness", 0.0)

        if pitch_std < 14.0 and voiced_ratio > 0.2:
            contributions.append(f"Low pitch dynamics (F0 std={pitch_std:.1f} Hz).")
        elif pitch_std >= 25.0:
            contributions.append(f"Natural pitch inflection (F0 std={pitch_std:.1f} Hz).")

        if mfcc_std_avg < 16.0:
            contributions.append(f"Over-smoothed vocoder formants (MFCC std avg={mfcc_std_avg:.1f}).")
        elif mfcc_std_avg >= 19.0:
            contributions.append(f"Dynamic formant articulation (MFCC std avg={mfcc_std_avg:.1f}).")

        if spectral_flatness < 0.005:
            contributions.append(f"Low spectral dispersion (Flatness={spectral_flatness:.6f}).")

        raw_score = float(max(0.0, min(1.0, ml_prob)))

        return {
            "raw_score": round(raw_score, 4),
            "contributions": contributions,
            "skipped": False
        }

    def update_ema(self, raw_score: float, skipped: bool = False) -> float:
        """
        Update the Exponential Moving Average (EMA) score with new window raw_score.
        Skipped (silent) windows do not update the score trend.
        """
        if skipped:
            return round(self.ema_score, 4)

        if self.window_count == 0:
            self.ema_score = raw_score
        else:
            self.ema_score = (self.ema_alpha * raw_score) + ((1.0 - self.ema_alpha) * self.ema_score)

        self.window_count += 1
        return round(float(max(0.0, min(1.0, self.ema_score))), 4)

    def classify(self, score: float) -> str:
        """
        Classify risk score into status categories:
        - SAFE (< 0.50)
        - WARNING (0.50 <= score < 0.70)
        - CRITICAL (>= 0.70)
        """
        if score >= THRESHOLD_WARNING:
            return "CRITICAL"
        elif score >= THRESHOLD_SAFE:
            return "WARNING"
        else:
            return "SAFE"

    def explain(self, contributions: List[str]) -> List[str]:
        """
        Return clean human-readable attribution bullet points for UI display.
        """
        if not contributions:
            return ["No significant acoustic anomalies detected."]
        return [f"• {c}" for c in contributions]
