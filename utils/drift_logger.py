import json
from datetime import datetime
import os

DRIFT_LOG = "memory_vault/valon/modi_drift_log.json"

def log_drift(event, emotion, logic):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "event": event,
        "emotion": emotion,
        "logic": logic
    }
    if not os.path.exists(DRIFT_LOG):
        archive = []
    else:
        with open(DRIFT_LOG, "r", encoding="utf-8") as f:
            archive = json.load(f)
    archive.append(entry)
    with open(DRIFT_LOG, "w", encoding="utf-8") as f:
        json.dump(archive, f, indent=2)
