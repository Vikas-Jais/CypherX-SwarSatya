"""
Tamper-evident local audit chain using SHA-256 hash-chaining.
"""

import json
import hashlib
import secrets
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Tuple
from config import LEDGER_PATH, PROTOTYPE_VERSION


def generate_pseudonymous_session_id() -> str:
    return f"sess_{secrets.token_hex(8)}"


def canonicalize_event(event_data: Dict[str, Any]) -> str:
    clean_dict = {k: v for k, v in event_data.items() if k != "record_hash"}
    return json.dumps(clean_dict, sort_keys=True, separators=(",", ":"))


def compute_record_hash(canonical_str: str) -> str:
    return hashlib.sha256(canonical_str.encode("utf-8")).hexdigest()


def get_last_record_hash(ledger_file: Path = LEDGER_PATH) -> str:
    ledger_file = Path(ledger_file)
    ledger_file.parent.mkdir(parents=True, exist_ok=True)

    if not ledger_file.exists():
        return "0" * 64

    last_line = ""
    with open(ledger_file, "r", encoding="utf-8") as f:
        for line in f:
            line_str = line.strip()
            if line_str:
                last_line = line_str

    if not last_line:
        return "0" * 64

    try:
        data = json.loads(last_line)
        return data.get("record_hash", "0" * 64)
    except Exception:
        return "0" * 64


def record_incident(
    final_risk_score: float,
    alert_level: str,
    session_id: str | None = None,
    ledger_file: Path = LEDGER_PATH
) -> Dict[str, Any]:
    ledger_file = Path(ledger_file)
    ledger_file.parent.mkdir(parents=True, exist_ok=True)

    if not session_id:
        session_id = generate_pseudonymous_session_id()

    event_id = f"evt_{secrets.token_hex(6)}"
    timestamp_utc = datetime.now(timezone.utc).isoformat()
    previous_hash = get_last_record_hash(ledger_file)

    event_dict: Dict[str, Any] = {
        "event_id": event_id,
        "timestamp_utc": timestamp_utc,
        "session_id": session_id,
        "final_risk_score": round(float(final_risk_score), 4),
        "alert_level": str(alert_level).upper(),
        "prototype_version": PROTOTYPE_VERSION,
        "previous_hash": previous_hash,
    }

    canonical_str = canonicalize_event(event_dict)
    record_hash = compute_record_hash(canonical_str)
    event_dict["record_hash"] = record_hash

    with open(ledger_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(event_dict, sort_keys=True) + "\n")

    return event_dict


def verify_ledger(ledger_file: Path = LEDGER_PATH) -> Tuple[bool, List[str]]:
    ledger_file = Path(ledger_file)
    ledger_file.parent.mkdir(parents=True, exist_ok=True)

    if not ledger_file.exists():
        return True, ["Ledger file does not exist yet (no records logged)."]

    errors: List[str] = []
    expected_previous_hash = "0" * 64

    line_number = 0
    with open(ledger_file, "r", encoding="utf-8") as f:
        for line in f:
            line_str = line.strip()
            if not line_str:
                continue

            line_number += 1
            try:
                record = json.loads(line_str)
            except Exception as e:
                errors.append(f"Line {line_number}: Invalid JSON syntax - {str(e)}")
                continue

            event_id = record.get("event_id", f"line_{line_number}")
            stored_record_hash = record.get("record_hash", "")
            stored_previous_hash = record.get("previous_hash", "")

            if stored_previous_hash != expected_previous_hash:
                errors.append(
                    f"Line {line_number} ({event_id}): Hash chain broken! "
                    f"Expected previous_hash '{expected_previous_hash[:12]}...', "
                    f"found '{stored_previous_hash[:12]}...'."
                )

            canonical_str = canonicalize_event(record)
            recomputed_hash = compute_record_hash(canonical_str)

            if recomputed_hash != stored_record_hash:
                errors.append(
                    f"Line {line_number} ({event_id}): Record data tampered! "
                    f"Stored record_hash '{stored_record_hash[:12]}...' does not match "
                    f"recomputed hash '{recomputed_hash[:12]}...'."
                )

            expected_previous_hash = stored_record_hash

    if line_number == 0:
        return True, ["Ledger is empty."]

    is_valid = len(errors) == 0
    return is_valid, errors


def load_ledger_records(ledger_file: Path = LEDGER_PATH) -> List[Dict[str, Any]]:
    ledger_file = Path(ledger_file)
    ledger_file.parent.mkdir(parents=True, exist_ok=True)

    if not ledger_file.exists():
        return []

    records = []
    with open(ledger_file, "r", encoding="utf-8") as f:
        for line in f:
            line_str = line.strip()
            if line_str:
                try:
                    records.append(json.loads(line_str))
                except Exception:
                    pass
    return records


def clear_ledger(ledger_file: Path = LEDGER_PATH) -> bool:
    ledger_file = Path(ledger_file)
    ledger_file.parent.mkdir(parents=True, exist_ok=True)

    if ledger_file.exists():
        try:
            ledger_file.unlink()
            return True
        except Exception:
            return False
    return True
