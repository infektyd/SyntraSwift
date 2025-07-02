# log_drift.py
import json
import os
from datetime import datetime

DRIFT_LOG_PATH = os.path.join("syntra_debug_logs", "drift_records.json")

def log_drift(input_text, valon_output, modi_output, final_drift_output, drift_ratio):
    drift_entry = {
        "timestamp": datetime.now().isoformat(),
        "input": input_text,
        "valon": valon_output,
        "modi": modi_output,
        "final_output": final_drift_output,
        "drift_ratio": drift_ratio
    }

    # Ensure the folder exists
    os.makedirs(os.path.dirname(DRIFT_LOG_PATH), exist_ok=True)

    # Append new drift entry
    if os.path.exists(DRIFT_LOG_PATH):
        with open(DRIFT_LOG_PATH, "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append(drift_entry)

    with open(DRIFT_LOG_PATH, "w") as f:
        json.dump(data, f, indent=2)

def read_drift_log():
    if os.path.exists(DRIFT_LOG_PATH):
        with open(DRIFT_LOG_PATH, "r") as f:
            return json.load(f)
    return []
