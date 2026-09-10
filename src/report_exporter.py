"""
Report Exporting module for SwarSatya application.
Exports window-by-window markings to CSV format and saves Matplotlib risk trajectory graphs
into timestamped test folders inside `data/reports/`.
"""

import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List
import pandas as pd
import matplotlib.pyplot as plt

from config import REPORTS_DIR


def sanitize_name(name: str) -> str:
    """Sanitize filename string for safe directory creation."""
    clean = re.sub(r'[^\w\s-]', '', str(name)).strip().replace(' ', '_')
    return clean if clean else "test_audio"


def export_scan_report(
    audio_filename: str,
    scan_results: List[Dict[str, Any]],
    final_score: float,
    final_status: str,
    fig,
    session_id: str = "SESSION-UNKNOWN"
) -> Dict[str, Any]:
    """
    Saves scan results CSV and Matplotlib graph PNG to timestamped test folder.
    Also appends to master CSV report.
    """
    now = datetime.now()
    timestamp_folder = now.strftime("%Y-%m-%d_%H-%M-%S")
    timestamp_utc = datetime.now(timezone.utc).isoformat()
    
    clean_name = sanitize_name(audio_filename)
    test_folder_name = f"{timestamp_folder}_{clean_name}"
    target_dir = REPORTS_DIR / test_folder_name
    target_dir.mkdir(parents=True, exist_ok=True)

    # 1. Save Detailed Window Scan Results CSV
    csv_file_path = target_dir / "scan_results.csv"
    if scan_results:
        df = pd.DataFrame(scan_results)
        export_df = pd.DataFrame()
        export_df["window_time_sec"] = df.get("time", 0.0)
        export_df["speech_activity_ratio"] = df.get("speech_activity", 0.0)
        export_df["raw_risk_score"] = df.get("raw_risk", 0.0)
        export_df["smoothed_risk_score"] = df.get("smoothed_risk", 0.0)
        export_df["alert_status"] = df.get("status", "SAFE")
        export_df["acoustic_attributions"] = df.get("contributions", []).apply(
            lambda c: " | ".join(c) if isinstance(c, list) else str(c)
        )
        export_df["test_audio_file"] = audio_filename
        export_df["timestamp_utc"] = timestamp_utc

        export_df.to_csv(csv_file_path, index=False, encoding="utf-8")
    else:
        pd.DataFrame(columns=[
            "window_time_sec", "speech_activity_ratio", "raw_risk_score",
            "smoothed_risk_score", "alert_status", "acoustic_attributions",
            "test_audio_file", "timestamp_utc"
        ]).to_csv(csv_file_path, index=False, encoding="utf-8")

    # 2. Save Risk Trajectory Graph PNG Image
    graph_file_path = target_dir / "risk_trajectory_graph.png"
    if fig:
        try:
            fig.savefig(graph_file_path, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
        except Exception:
            pass

    # 3. Append to Master Scan History CSV
    master_csv_path = REPORTS_DIR / "master_scan_history.csv"
    master_row = {
        "test_name": clean_name,
        "audio_file": audio_filename,
        "timestamp_date": now.strftime("%Y-%m-%d %H:%M:%S"),
        "timestamp_utc": timestamp_utc,
        "session_id": session_id,
        "final_risk_score_pct": f"{final_score * 100:.1f}%",
        "verdict_status": final_status,
        "total_windows_scanned": len(scan_results),
        "detail_csv_path": str(csv_file_path.resolve()),
        "graph_image_path": str(graph_file_path.resolve()),
        "report_folder": str(target_dir.resolve())
    }

    if master_csv_path.exists():
        try:
            master_df = pd.read_csv(master_csv_path)
            master_df = pd.concat([master_df, pd.DataFrame([master_row])], ignore_index=True)
        except Exception:
            master_df = pd.DataFrame([master_row])
    else:
        master_df = pd.DataFrame([master_row])

    master_df.to_csv(master_csv_path, index=False, encoding="utf-8")

    return {
        "test_name": clean_name,
        "folder_path": target_dir,
        "csv_path": csv_file_path,
        "graph_path": graph_file_path,
        "master_csv": master_csv_path
    }
