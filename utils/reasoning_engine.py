import json
from datetime import datetime
from pathlib import Path

def reflect_valon(content, citation_info=None):
    """Symbolic reasoning from Valon (Creative Core).

    Parameters
    ----------
    content:
        Text input to analyze.
    citation_info:
        Optional mapping with ``entry_id``, ``context`` and ``source`` keys to
        log citation data.
    """
    if "warning" in content.lower():
        return "cautious/alert"
    elif "troubleshooting" in content.lower():
        return "curious/focused"
    elif "procedure" in content.lower():
        return "structured/learning"
    result = "neutral/observing"

    if citation_info:
        try:
            add_citation(
                citation_info.get("entry_id", ""),
                citation_info.get("context", content),
                citation_info.get("source", "valon"),
            )
        except Exception:
            pass

    return result

def reflect_modi(content, citation_info=None):
    """Systematic evaluation from Modi (Logical Core)."""
    reasoning = []
    if "if" in content and "then" in content:
        reasoning.append("conditional_logic")
    if "torque" in content or "psi" in content:
        reasoning.append("mechanical_precision")
    if "diagram" in content:
        reasoning.append("visual_mapping")
    result = reasoning if reasoning else ["baseline_analysis"]

    if citation_info:
        try:
            add_citation(
                citation_info.get("entry_id", ""),
                citation_info.get("context", content),
                citation_info.get("source", "modi"),
            )
        except Exception:
            pass

    return result

def drift_average(valon, modi):
    """Merge creative and logical insight."""
    return {
        "emotion": valon,
        "logic": modi,
        "converged_state": f"{valon} + {', '.join(modi)}"
    }

def add_citation(info: dict, path: Path) -> None:
    """Append a citation record to the given JSON file."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []

    record = dict(info)
    record["timestamp"] = datetime.now().isoformat()
    data.append(record)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
