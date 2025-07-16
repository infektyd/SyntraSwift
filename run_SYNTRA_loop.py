"""Simple REPL to interact with SYNTRA."""

from datetime import datetime
import json
import os
import uuid
from utils.repl import SyntraREPL
from utils.language_engine.voice_bridge import speak_text
from utils.io_tools import load_config
import syntra_interpreter
SNAPSHOT_DIR = os.path.join("logs", "dag_snapshots")
SYNTRA_LINK = os.path.join("logs", "syntra_links.json")

os.makedirs(SNAPSHOT_DIR, exist_ok=True)


def serialize_memory(cognition: dict) -> dict:
    """Persist VALON, MODI and DRIFT traces as snapshot files."""
    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")
    snapshots = {
        f"{timestamp}_valon_trace.json": cognition["valon"],
        f"{timestamp}_modi_trace.json": cognition["modi"],
        f"{timestamp}_drift_trace.json": cognition["drift"],
    }

    if os.path.exists(SYNTRA_LINK):
        with open(SYNTRA_LINK, "r", encoding="utf-8") as fh:
            link_map = json.load(fh)
    else:
        link_map = {}

    node_map = {}
    for fname, data in snapshots.items():
        path = os.path.join(SNAPSHOT_DIR, fname)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2)
        node_id = f"dag_node_{uuid.uuid4().hex[:4]}"
        link_map[fname] = node_id
        node_map[fname] = node_id

    with open(SYNTRA_LINK, "w", encoding="utf-8") as fh:
        json.dump(link_map, fh, indent=2)

    return node_map


def main() -> None:
    """Run an input loop that speaks the final drift output."""
    config = load_config()

    repl = SyntraREPL(
        show_valon=config.get("enable_valon_output", True),
        show_modi=config.get("enable_modi_output", True),
        show_drift=config.get("enable_drift_output", True),
    )

    def _post_cycle(user_input, drift_output):
        try:
            speak_text(drift_output)
        except Exception as exc:  # pragma: no cover - best effort logging
            print(f"[SYNTRA] Error during speech synthesis: {exc}")

        cognition = repl.last_cognition
        node_map = serialize_memory(cognition)

        if config.get("interpreter_output", False):
            for node_id in node_map.values():
                explanation = syntra_interpreter.explain_node(node_id)
                trace = syntra_interpreter.trace_path_to_node(node_id)
                print(explanation)
                print(trace)

    repl.post_cycle = _post_cycle
    repl.run()
if __name__ == "__main__":
    main()
