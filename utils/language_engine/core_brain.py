# Stub out get_logical_assertion so pdf_ingestor can import it
def get_logical_assertion(*args, **kwargs):
    return None

# core_brain.py
from utils.language_engine import (
    reflect_valon,
    reflect_modi,
    drift_average,
    query_apple_llm,
)
from utils.symbolic_drift import log_symbolic_drift
from utils.io_tools import load_config
import json
import os
from datetime import datetime


ENTROPY_DIR = "entropy_logs"
DRIFT_DIR = "drift_logs"

os.makedirs(ENTROPY_DIR, exist_ok=True)
os.makedirs(DRIFT_DIR, exist_ok=True)


def _log_stage(stage: str, output, directory: str) -> None:
    """Append stage output to a log file."""
    log_path = os.path.join(directory, f"{stage}.json")
    entry = {"timestamp": datetime.now().isoformat(), "output": output}

    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []

    data.append(entry)
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def _valon_stage(input_text, citation_info=None):
    """Run VALON reflection and log the result."""
    output = reflect_valon(input_text, citation_info=citation_info)
    _log_stage("valon_stage", output, ENTROPY_DIR)
    return output


def _modi_stage(input_text, citation_info=None):
    """Run MODI reflection and log the result."""
    output = reflect_modi(input_text, citation_info=citation_info)
    _log_stage("modi_stage", output, ENTROPY_DIR)
    return output


def _drift_stage(valon_output, modi_output):
    """Synthesize VALON and MODI outputs and log the drift result."""
    drift_output = drift_average(valon_output, modi_output)
    _log_stage("drift_stage", drift_output, DRIFT_DIR)
    return drift_output

def process_through_brains(input_data, citation_info=None):
    """Run the VALON, MODI and DRIFT stages in sequence."""
    cfg = load_config()
    valon_output = _valon_stage(input_data, citation_info=citation_info)
    modi_output = _modi_stage(input_data, citation_info=citation_info)
    drift_output = _drift_stage(valon_output, modi_output)

    # Track drift between flat vault and DAG snapshot
    log_symbolic_drift(valon_output, modi_output)

    if cfg.get("use_apple_llm"):
        try:
            query_apple_llm(
                input_data,
                api_key=cfg.get("apple_llm_api_key"),
                base_url=cfg.get("apple_llm_api_base"),
            )
        except Exception:
            pass

    return {
        "valon": valon_output,
        "modi": modi_output,
        "drift": drift_output,
    }



def symbolic_dream_loop():
    """Blend recent VALON symbols with MODI fault logs to create drift."""
    valon_path = os.path.join(
        "memory_vault", "valon", "valon_symbolic_archive.json"
    )
    if os.path.exists(valon_path):
        with open(valon_path, "r", encoding="utf-8") as f:
            v_data = json.load(f)
        events = v_data.get("symbolic_events", [])
    else:
        events = []

    valon_terms = []
    structures = []
    for e in events[-3:]:
        refl = e.get("reflected", {})
        valon_terms.extend(refl.get("symbolic_terms", []))
        if refl.get("structure"):
            structures.append(refl.get("structure"))

    modi_log_path = os.path.join(
        "memory_vault", "modi", "modi_fault_logs.json"
    )
    if os.path.exists(modi_log_path):
        with open(modi_log_path, "r", encoding="utf-8") as f:
            modi_logs = json.load(f)
    else:
        modi_logs = []

    fault_phrases = [entry.get("fault", "") for entry in modi_logs[-3:]]

    unique_terms = []
    for t in valon_terms:
        if t not in unique_terms:
            unique_terms.append(t)

    structure = structures[-1] if structures else "procedural/informative"
    dream_output = f"[{structure}] " + " ".join(unique_terms + fault_phrases)

    _log_stage("symbolic_dream_loop", dream_output, DRIFT_DIR)
    return dream_output
