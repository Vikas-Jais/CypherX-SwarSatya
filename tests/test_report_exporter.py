"""
Unit tests for scan report CSV & graph exporter module.
"""

import sys
from pathlib import Path
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.report_exporter import export_scan_report, sanitize_name


def test_sanitize_name():
    """Verify filename sanitization function."""
    assert sanitize_name("Test File 123!.wav") == "Test_File_123wav"
    assert sanitize_name("   AI Demo   ") == "AI_Demo"
    assert sanitize_name("???") == "test_audio"


def test_export_scan_report(tmp_path, monkeypatch):
    """Test CSV and folder creation for test scan exports."""
    import config
    monkeypatch.setattr(config, "REPORTS_DIR", tmp_path / "reports")

    mock_scan_results = [
        {
            "time": 0.25,
            "speech_activity": 0.85,
            "raw_risk": 0.3,
            "smoothed_risk": 0.35,
            "status": "SAFE",
            "contributions": ["Pitch normal", "ZCR stable"]
        },
        {
            "time": 0.50,
            "speech_activity": 0.90,
            "raw_risk": 0.8,
            "smoothed_risk": 0.65,
            "status": "WARNING",
            "contributions": ["MFCC variance high"]
        }
    ]

    info = export_scan_report(
        audio_filename="Unit_Test_Recording.wav",
        scan_results=mock_scan_results,
        final_score=0.65,
        final_status="WARNING",
        fig=None,
        session_id="SES-UNITTEST"
    )

    assert info["folder_path"].exists()
    assert info["csv_path"].exists()
    assert info["master_csv"].exists()

    # Check contents of generated scan_results.csv
    import pandas as pd
    df = pd.read_csv(info["csv_path"])
    assert len(df) == 2
    assert "window_time_sec" in df.columns
    assert "smoothed_risk_score" in df.columns
    assert df["alert_status"].tolist() == ["SAFE", "WARNING"]

    # Check contents of master_scan_history.csv
    master_df = pd.read_csv(info["master_csv"])
    assert len(master_df) >= 1
    assert "Unit_Test_Recording.wav" in master_df["audio_file"].values
