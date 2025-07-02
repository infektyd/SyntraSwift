import json
import os
from datetime import datetime

LOG_DIR = os.path.join('logs', 'interpreter')
os.makedirs(LOG_DIR, exist_ok=True)


def _write_log(entry):
    timestamp = datetime.now().strftime('%Y%m%dT%H%M%S')
    path = os.path.join(LOG_DIR, f"{timestamp}_interpreter_log.json")
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(entry, f, indent=2)


def explain_node(node_id):
    """Return a placeholder explanation for a DAG node."""
    explanation = f"Explanation for {node_id}"
    _write_log({"action": "explain", "node_id": node_id, "output": explanation})
    return explanation


def trace_path_to_node(node_id):
    """Return a symbolic path leading to the node."""
    path = f"root -> {node_id}"
    _write_log({"action": "trace", "node_id": node_id, "output": path})
    return path


def list_recent_drift_links():
    """Return a dictionary of recent drift snapshot links."""
    links = {}
    _write_log({"action": "list_drift", "output": links})
    return links
