"""
Deterministic mock data provider for SwarSatya Public Safety UI Prototype.
Contains fixed, pre-calculated scenario vectors, mock ledger chain, and threat insights.
No random generators or non-deterministic calls are used.
"""

import hashlib
from typing import Dict, Any, List

# ------------------------------------------------------------------------------
# SHA-256 HASH UTILITY
# ------------------------------------------------------------------------------
def compute_sha256(text: str) -> str:
    """Return deterministic 64-character hex SHA-256 digest of input string."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

# ------------------------------------------------------------------------------
# DEMO SCENARIO 1: GENUINE HUMAN VOICE
# ------------------------------------------------------------------------------
GENUINE_HUMAN_SCENARIO: Dict[str, Any] = {
    "key": "human",
    "title": "Genuine Human Voice",
    "status_color": "green",
    "description": "Simulated natural voice characteristics with variable pitch and timing.",
    "source_line": "Source: Local prepared demonstration asset · No persistent audio retention",
    "steps": 15,
    "raw_scores": [0.15, 0.18, 0.22, 0.14, 0.31, 0.28, 0.19, 0.35, 0.24, 0.40, 0.33, 0.27, 0.21, 0.30, 0.25],
    "smoothed_scores": [0.15, 0.16, 0.18, 0.17, 0.22, 0.24, 0.22, 0.27, 0.26, 0.31, 0.32, 0.30, 0.27, 0.28, 0.27],
    "speech_activities": [82, 85, 88, 86, 90, 89, 87, 91, 88, 85, 87, 89, 86, 88, 87],
    "pitch_stds": [35.2, 38.4, 32.1, 41.0, 37.6, 29.8, 36.4, 42.1, 33.9, 39.5, 36.1, 34.8, 37.2, 38.0, 35.6],
    "spectral_flatness": [0.018, 0.021, 0.016, 0.025, 0.019, 0.015, 0.022, 0.027, 0.017, 0.024, 0.020, 0.019, 0.023, 0.021, 0.018],
    "timing_regularity": [42, 45, 48, 40, 52, 49, 46, 55, 47, 58, 51, 48, 44, 50, 47],
    "noise_influences": [12, 14, 11, 15, 13, 10, 14, 16, 12, 15, 13, 11, 14, 13, 12],
    "final_smoothed_score": 0.27,
    "final_status": "SAFE",
    "explanations": [
        "Natural pitch variation observed across voice frames (F0 std = 35.6 Hz).",
        "Variable formant articulation profiles consistent with organic speech (MFCC std = 24.1).",
        "No sustained flat pitch or unnatural spectral regularity detected."
    ]
}

# ------------------------------------------------------------------------------
# DEMO SCENARIO 2: SYNTHETIC VOICE PATTERN
# ------------------------------------------------------------------------------
SYNTHETIC_PATTERN_SCENARIO: Dict[str, Any] = {
    "key": "synthetic",
    "title": "Synthetic Voice Pattern",
    "status_color": "red",
    "description": "Simulated highly regular acoustic patterns intended to demonstrate a high-risk flow.",
    "source_line": "Source: Local prepared demonstration asset · No persistent audio retention",
    "steps": 15,
    "raw_scores": [0.46, 0.52, 0.58, 0.64, 0.69, 0.73, 0.78, 0.82, 0.85, 0.88, 0.90, 0.91, 0.92, 0.93, 0.93],
    "smoothed_scores": [0.46, 0.48, 0.52, 0.56, 0.61, 0.65, 0.70, 0.74, 0.78, 0.81, 0.84, 0.87, 0.89, 0.90, 0.89],
    "speech_activities": [88, 90, 92, 91, 93, 94, 95, 96, 95, 96, 97, 96, 95, 96, 95],
    "pitch_stds": [12.4, 9.8, 7.2, 5.8, 4.9, 4.1, 3.8, 3.5, 3.2, 3.1, 3.0, 3.1, 3.0, 3.2, 3.1],
    "spectral_flatness": [0.0042, 0.0035, 0.0028, 0.0021, 0.0018, 0.0015, 0.0012, 0.0010, 0.0009, 0.0008, 0.0008, 0.0008, 0.0007, 0.0008, 0.0008],
    "timing_regularity": [78, 82, 85, 89, 91, 93, 95, 96, 97, 97, 98, 98, 97, 98, 98],
    "noise_influences": [8, 7, 6, 5, 5, 4, 4, 3, 3, 3, 2, 2, 2, 2, 2],
    "final_smoothed_score": 0.89,
    "final_status": "CRITICAL",
    "explanations": [
        "Unusually stable pitch contour detected across consecutive frames (F0 std = 3.1 Hz).",
        "Over-smoothed vocoder formants (MFCC std avg = 10.4).",
        "Sustained high temporal regularity across consecutive 1-second analysis windows."
    ]
}

# ------------------------------------------------------------------------------
# DEMO SCENARIO 3: NOISY CALL ENVIRONMENT
# ------------------------------------------------------------------------------
NOISY_ENVIRONMENT_SCENARIO: Dict[str, Any] = {
    "key": "noisy",
    "title": "Noisy Call Environment",
    "status_color": "amber",
    "description": "Simulated background noise and uncertain signal quality.",
    "source_line": "Source: Local prepared demonstration asset · No persistent audio retention",
    "steps": 15,
    "raw_scores": [0.38, 0.45, 0.52, 0.48, 0.61, 0.55, 0.68, 0.59, 0.64, 0.58, 0.62, 0.51, 0.47, 0.56, 0.54],
    "smoothed_scores": [0.38, 0.40, 0.44, 0.45, 0.51, 0.52, 0.58, 0.58, 0.60, 0.59, 0.60, 0.57, 0.54, 0.55, 0.55],
    "speech_activities": [65, 68, 72, 70, 75, 73, 76, 74, 78, 75, 77, 72, 69, 74, 73],
    "pitch_stds": [22.1, 19.8, 18.5, 21.0, 17.6, 16.4, 15.2, 18.1, 16.9, 17.5, 18.2, 20.1, 21.8, 19.4, 18.8],
    "spectral_flatness": [0.038, 0.042, 0.048, 0.045, 0.052, 0.056, 0.062, 0.058, 0.061, 0.055, 0.059, 0.049, 0.043, 0.051, 0.048],
    "timing_regularity": [62, 65, 68, 66, 71, 70, 74, 72, 75, 73, 74, 69, 66, 71, 70],
    "noise_influences": [65, 68, 72, 70, 78, 75, 82, 79, 84, 80, 81, 73, 67, 76, 74],
    "final_smoothed_score": 0.55,
    "final_status": "WARNING",
    "explanations": [
        "High ambient noise floor increasing signal uncertainty.",
        "Moderate pitch variance with frame-boundary fluctuations.",
        "Signal noise reduces classification certainty; secondary verification is recommended."
    ]
}

# Map key to scenario dictionary
SCENARIOS: Dict[str, Dict[str, Any]] = {
    "human": GENUINE_HUMAN_SCENARIO,
    "synthetic": SYNTHETIC_PATTERN_SCENARIO,
    "noisy": NOISY_ENVIRONMENT_SCENARIO
}

# ------------------------------------------------------------------------------
# INITIAL DETERMINISTIC MOCK LEDGER CHAIN
# ------------------------------------------------------------------------------
def get_initial_ledger() -> List[Dict[str, Any]]:
    """Return deterministic baseline hash-chained ledger records."""
    gen_prev = "0" * 64
    r1_data = "SS-REG-2026-001|2026-03-10 10:15:22|SS-DEMO-001|0.27|SAFE|" + gen_prev
    r1_hash = compute_sha256(r1_data)

    r2_data = "SS-REG-2026-002|2026-03-10 11:30:45|SS-DEMO-002|0.89|CRITICAL|" + r1_hash
    r2_hash = compute_sha256(r2_data)

    r3_data = "SS-REG-2026-003|2026-03-10 14:05:12|SS-DEMO-003|0.55|WARNING|" + r2_hash
    r3_hash = compute_sha256(r3_data)

    r4_data = "SS-REG-2026-004|2026-03-10 16:42:00|SS-DEMO-004|0.24|SAFE|" + r3_hash
    r4_hash = compute_sha256(r4_data)

    return [
        {
            "register_id": "SS-REG-2026-001",
            "recorded_time": "2026-03-10 10:15:22",
            "session_ref": "SS-DEMO-001",
            "risk_indicator": 0.27,
            "advisory_level": "SAFE",
            "prev_hash": gen_prev,
            "event_hash": r1_hash,
            "integrity_status": "Valid Link"
        },
        {
            "register_id": "SS-REG-2026-002",
            "recorded_time": "2026-03-10 11:30:45",
            "session_ref": "SS-DEMO-002",
            "risk_indicator": 0.89,
            "advisory_level": "CRITICAL",
            "prev_hash": r1_hash,
            "event_hash": r2_hash,
            "integrity_status": "Valid Link"
        },
        {
            "register_id": "SS-REG-2026-003",
            "recorded_time": "2026-03-10 14:05:12",
            "session_ref": "SS-DEMO-003",
            "risk_indicator": 0.55,
            "advisory_level": "WARNING",
            "prev_hash": r2_hash,
            "event_hash": r3_hash,
            "integrity_status": "Valid Link"
        },
        {
            "register_id": "SS-REG-2026-004",
            "recorded_time": "2026-03-10 16:42:00",
            "session_ref": "SS-DEMO-004",
            "risk_indicator": 0.24,
            "advisory_level": "SAFE",
            "prev_hash": r3_hash,
            "event_hash": r4_hash,
            "integrity_status": "Valid Link"
        }
    ]

# ------------------------------------------------------------------------------
# THREAT INSIGHTS MOCK DATA
# ------------------------------------------------------------------------------
INITIAL_THREAT_KPIS = {
    "total_scans": 142,
    "safe_outcomes": 98,
    "warning_advisories": 26,
    "critical_advisories": 18
}

THREAT_DISTRIBUTION_DATA = [
    {"Advisory Level": "SAFE", "Count": 98, "Color": "#15803D"},
    {"Advisory Level": "WARNING", "Count": 26, "Color": "#B45309"},
    {"Advisory Level": "CRITICAL", "Count": 18, "Color": "#B91C1C"}
]

THREAT_CONDITION_DATA = [
    {"Scenario Condition": "Genuine Human", "Average Risk Score (%)": 26.5},
    {"Scenario Condition": "Noisy Environment", "Average Risk Score (%)": 54.2},
    {"Scenario Condition": "Synthetic Voice Pattern", "Average Risk Score (%)": 87.8}
]

THREAT_TREND_DATA = [
    {"Session": "S-01", "Average Risk": 0.22, "Type": "Human"},
    {"Session": "S-02", "Average Risk": 0.31, "Type": "Human"},
    {"Session": "S-03", "Average Risk": 0.88, "Type": "Synthetic"},
    {"Session": "S-04", "Average Risk": 0.52, "Type": "Noisy"},
    {"Session": "S-05", "Average Risk": 0.24, "Type": "Human"},
    {"Session": "S-06", "Average Risk": 0.91, "Type": "Synthetic"},
    {"Session": "S-07", "Average Risk": 0.58, "Type": "Noisy"},
    {"Session": "S-08", "Average Risk": 0.28, "Type": "Human"},
    {"Session": "S-09", "Average Risk": 0.86, "Type": "Synthetic"},
    {"Session": "S-10", "Average Risk": 0.25, "Type": "Human"}
]

LANGUAGE_ROADMAP = [
    "Hindi",
    "Hinglish",
    "Marathi",
    "Tamil",
    "Bengali",
    "Telugu",
    "Gujarati",
    "Kannada"
]
