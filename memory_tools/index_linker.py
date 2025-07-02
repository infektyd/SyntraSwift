import json
import os
import uuid

LINKMAP_PATH = os.path.join("memory_vault", "linkmap.json")


def _load_map():
    if os.path.exists(LINKMAP_PATH):
        with open(LINKMAP_PATH, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except Exception:
                return {"json_to_dag": {}, "dag_to_json": {}}
    return {"json_to_dag": {}, "dag_to_json": {}}


def _save_map(data):
    os.makedirs(os.path.dirname(LINKMAP_PATH), exist_ok=True)
    with open(LINKMAP_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def assign_uid(memory_entry: dict) -> str:
    """Append a unique identifier to a memory entry."""
    uid = str(uuid.uuid4())
    memory_entry["uid"] = uid
    return uid


def create_link(json_path: str, dag_node_id: str) -> None:
    """Store a bidirectional mapping between JSON file and DAG node."""
    data = _load_map()
    data.setdefault("json_to_dag", {})[json_path] = dag_node_id
    data.setdefault("dag_to_json", {})[dag_node_id] = json_path
    _save_map(data)
