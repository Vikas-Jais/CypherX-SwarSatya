"""
Configuration settings for SwarSatya (स्वरसत्य) — Voice Truth prototype.
"""

from pathlib import Path
import tempfile

# Base Paths
BASE_DIR = Path(__file__).resolve().parent

def get_writable_data_dir() -> Path:
    """
    Return a guaranteed writable directory for audit logs and synthetic demo audio.
    Tries workspace directory first, then falls back to user home ~/.swarsatya/data
    to bypass OneDrive file lock / ACL restrictions on Windows.
    """
    local_data = BASE_DIR / "data"
    try:
        local_data.mkdir(parents=True, exist_ok=True)
        test_file = local_data / ".write_test"
        test_file.write_text("test", encoding="utf-8")
        test_file.unlink()
        return local_data
    except Exception:
        fallback_data = Path.home() / ".swarsatya" / "data"
        fallback_data.mkdir(parents=True, exist_ok=True)
        return fallback_data

DATA_DIR = get_writable_data_dir()
LEDGER_PATH = DATA_DIR / "incident_ledger.jsonl"
REPORTS_DIR = DATA_DIR / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# Application Metadata & Versioning
PROTOTYPE_VERSION = "1.0.0"
APP_NAME = "SwarSatya — Voice Security Engine"
TAGLINE = "Real-Time AI Voice Authentication & Tamper-Evident Incident Audit"

# Modern Dark Theme Color Palette
COLOR_DEEP_BLUE = "#1E3A8A"
COLOR_ACCENT_BLUE = "#2563EB"
COLOR_CYAN = "#38BDF8"
COLOR_ORANGE = "#F97316"
COLOR_GREEN = "#10B981"
COLOR_RED = "#EF4444"
COLOR_BG_DARK = "#090D16"
COLOR_CARD_BG = "#111827"
COLOR_CARD_BORDER = "#1F2937"
COLOR_TEXT_PRIMARY = "#F8FAFC"
COLOR_TEXT_MUTED = "#94A3B8"

# Audio Pipeline Settings
TARGET_SR = 16000           # Sample rate in Hz
WINDOW_SECONDS = 1.0        # Sliding window length in seconds
HOP_SECONDS = 0.25          # Sliding window hop size in seconds
MIN_SPEECH_RMS = 0.015      # RMS threshold below which window is considered silent

# Calibrated Differential Risk Thresholds (SAFE < 0.50, WARNING 0.50-0.70, CRITICAL >= 0.70)
THRESHOLD_SAFE = 0.50
THRESHOLD_WARNING = 0.70
EMA_ALPHA = 0.35            # Exponential Moving Average factor

# Heuristic Score Weights & Base Score
BASE_HEURISTIC_SCORE = 0.20
WEIGHT_PITCH_CONSTANCY = 0.25
WEIGHT_SPECTRAL_FLATNESS = 0.25
WEIGHT_FRAME_REGULARITY = 0.25
