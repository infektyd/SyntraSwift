import json
import os
from datetime import datetime
from utils.io_tools import load_config

FLAT_VAULT = os.path.join("memory_vault", "valon", "valon_symbolic_archive.json")
PREV_SNAPSHOT = os.path.join("logs", "prev_valon_snapshot.json")
DIFF_LOG = os.path.join("logs", "symbolic_drift.json")


def _load_json(path, default):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def log_symbolic_drift(valon_output, modi_output):
    """Diff flat vault and DAG snapshot after cognition cycle."""
    config = load_config()
    if not config.get("log_symbolic_drift", True):
        return

    os.makedirs("logs", exist_ok=True)

    current = _load_json(FLAT_VAULT, {"symbolic_events": []})
    previous = _load_json(PREV_SNAPSHOT, {"symbolic_events": []})

    prev_sources = {e.get("source") for e in previous.get("symbolic_events", [])}
    curr_sources = {e.get("source") for e in current.get("symbolic_events", [])}

    new_events = [e for e in current.get("symbolic_events", []) if e.get("source") not in prev_sources]
    removed_events = [e for e in previous.get("symbolic_events", []) if e.get("source") not in curr_sources]

    diff_entry = {
        "timestamp": datetime.now().isoformat(),
        "new_events": new_events,
        "removed_events": removed_events,
        "valon_trace": valon_output,
        "modi_trace": modi_output,
    }

    log = _load_json(DIFF_LOG, [])
    log.append(diff_entry)
    with open(DIFF_LOG, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2)

    with open(PREV_SNAPSHOT, "w", encoding="utf-8") as f:
        json.dump(current, f, indent=2)

