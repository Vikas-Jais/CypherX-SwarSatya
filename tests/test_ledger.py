"""
Unit tests for tamper-evident SHA-256 local audit ledger module.
"""

import sys
import json
from pathlib import Path
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.ledger import (
    record_incident,
    verify_ledger,
    clear_ledger,
    load_ledger_records
)


def test_create_and_verify_ledger(tmp_path):
    """Write 3 records to a temporary ledger file and verify cryptographic hash chain."""
    temp_ledger = tmp_path / "test_ledger.jsonl"

    rec1 = record_incident(final_risk_score=0.45, alert_level="SAFE", session_id="sess_test1", ledger_file=temp_ledger)
    rec2 = record_incident(final_risk_score=0.72, alert_level="WARNING", session_id="sess_test2", ledger_file=temp_ledger)
    rec3 = record_incident(final_risk_score=0.91, alert_level="CRITICAL", session_id="sess_test3", ledger_file=temp_ledger)

    assert temp_ledger.exists()

    # Verify link chain
    assert rec1["previous_hash"] == "0" * 64
    assert rec2["previous_hash"] == rec1["record_hash"]
    assert rec3["previous_hash"] == rec2["record_hash"]

    is_valid, errors = verify_ledger(temp_ledger)
    assert is_valid is True
    assert len(errors) == 0


def test_tamper_detection(tmp_path):
    """Modify one line in a temporary ledger file and assert that verification fails."""
    temp_ledger = tmp_path / "tamper_ledger.jsonl"

    record_incident(final_risk_score=0.30, alert_level="SAFE", session_id="sess_101", ledger_file=temp_ledger)
    rec2 = record_incident(final_risk_score=0.88, alert_level="CRITICAL", session_id="sess_102", ledger_file=temp_ledger)
    record_incident(final_risk_score=0.20, alert_level="SAFE", session_id="sess_103", ledger_file=temp_ledger)

    # Initial ledger should be valid
    is_valid_initial, _ = verify_ledger(temp_ledger)
    assert is_valid_initial is True

    # Tamper with line 2: change final_risk_score from 0.88 to 0.10 (malicious alteration)
    lines = []
    with open(temp_ledger, "r", encoding="utf-8") as f:
        lines = f.readlines()

    tampered_dict = json.loads(lines[1])
    tampered_dict["final_risk_score"] = 0.10  # Alter score without recomputing SHA-256
    lines[1] = json.dumps(tampered_dict, sort_keys=True) + "\n"

    with open(temp_ledger, "w", encoding="utf-8") as f:
        f.writelines(lines)

    # Verify that tamper detection catches the alteration
    is_valid_after_tamper, errors = verify_ledger(temp_ledger)
    assert is_valid_after_tamper is False
    assert len(errors) > 0
    assert any(rec2["event_id"] in err or "tampered" in err.lower() for err in errors)
