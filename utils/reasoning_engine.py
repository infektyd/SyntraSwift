import json
import subprocess
from datetime import datetime
from pathlib import Path

SWIFT_PACKAGE = Path(__file__).resolve().parent.parent

# The Python layer relies on the SyntraSwift package for symbolic reasoning.

def _run_swift(command: str, *args: str) -> str:
    """Execute the SyntraSwift CLI with the given command."""
    cmd = [
        "swift",
        "run",
        "--package-path",
        str(SWIFT_PACKAGE),
        "SyntraSwiftCLI",
        command,
    ]
    cmd.extend(args)
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return result.stdout.strip()

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
    result = _run_swift("reflect_valon", content)

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
    output = _run_swift("reflect_modi", content)
    try:
        result = json.loads(output)
    except Exception:
        result = []

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
    output = _run_swift("drift_average", valon, json.dumps(modi))
    try:
        return json.loads(output)
    except Exception:
        return {}

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
