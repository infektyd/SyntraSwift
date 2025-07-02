from pathlib import Path
from typing import Any, Optional

from utils.reasoning_engine import add_citation

DEFAULT_CITATION_PATH = Path("entropy_logs/citations.json")

def citation_handler(response: Any, citation_info: Optional[dict] = None, citation_path: Path = DEFAULT_CITATION_PATH):
    """Handle citation recording if citation_info is provided."""
    if citation_info:
        add_citation(citation_info, citation_path)
    return response
