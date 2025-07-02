import json
import os
import uuid
from pathlib import Path

from utils.io_tools import load_config

HYBRID_DIR = Path("memory_vault/hybrid_store")
NODES_FILE = HYBRID_DIR / "graph_nodes.json"
EDGES_FILE = HYBRID_DIR / "edges_map.json"
INDEX_FILE = HYBRID_DIR / "hybrid_index.json"


def _load_json(path):
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def _save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def init_hybrid_store():
    """Ensure hybrid storage files exist."""
    HYBRID_DIR.mkdir(parents=True, exist_ok=True)
    for p in (NODES_FILE, EDGES_FILE, INDEX_FILE):
        if not p.exists():
            _save_json(p, {})


def add_memory_node(entry, references=None):
    """Add a memory entry to the hybrid graph and return its UID."""
    config = load_config()
    if config.get("memory_mode", "flat") != "hybrid":
        return None

    init_hybrid_store()
    uid = str(uuid.uuid4())
    nodes = _load_json(NODES_FILE)
    nodes[uid] = {
        "uid": uid,
        "timestamp": entry.get("timestamp"),
        "path": entry.get("source"),
        "summary": entry.get("summary", "")[:200],
    }
    _save_json(NODES_FILE, nodes)

    edges = _load_json(EDGES_FILE)
    edges[uid] = references or []
    _save_json(EDGES_FILE, edges)

    index = _load_json(INDEX_FILE)
    src = entry.get("source") or "unknown"
    index.setdefault(src, []).append(uid)
    _save_json(INDEX_FILE, index)
    return uid


def traverse_memory():
    """Yield memory entries according to the configured mode."""
    config = load_config()
    mode = config.get("memory_mode", "flat")

    if mode == "hybrid":
        init_hybrid_store()
        nodes = _load_json(NODES_FILE)
        for node in nodes.values():
            yield node
    else:
        for vault in [Path("memory_vault/modi"), Path("memory_vault/valon")]:
            if not vault.exists():
                continue
            for file in vault.glob("*.json"):
                with open(file, "r", encoding="utf-8") as f:
                    try:
                        data = json.load(f)
                        yield data
                    except Exception:
                        continue

