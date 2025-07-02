import os
import json
from datetime import datetime

ENTROPY_DIR = "entropy_logs"

def log_entropy_drift(reason: str, source_filename: str):
    os.makedirs(ENTROPY_DIR, exist_ok=True)

    entry = {
        "timestamp": datetime.now().isoformat(),
        "source": source_filename,
        "reason": reason,
        "flag": "entropy_drift"
    }

    out_path = os.path.join(ENTROPY_DIR, f"{reason.replace(' ', '_')}.json")

    # Append or create JSON log
    if os.path.exists(out_path):
        with open(out_path, "r", encoding="utf-8") as f:
            logs = json.load(f)
    else:
        logs = []

    logs.append(entry)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2)


def trigger_dream(reason: str, source_filename: str):
    """Log a dream trigger event when entropy reaches a threshold."""
    os.makedirs(ENTROPY_DIR, exist_ok=True)

    entry = {
        "timestamp": datetime.now().isoformat(),
        "source": source_filename,
        "reason": reason,
        "flag": "dream_triggered",
    }

    out_path = os.path.join(ENTROPY_DIR, "dream_triggers.json")

    if os.path.exists(out_path):
        with open(out_path, "r", encoding="utf-8") as f:
            logs = json.load(f)
    else:
        logs = []

    logs.append(entry)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2)

    print(f"[ENTROPY] Dream triggered due to {reason} from {source_filename}")
