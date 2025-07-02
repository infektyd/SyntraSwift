import json
from pathlib import Path
from unittest.mock import patch

# Ensure utils package is importable
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.citation_handler import citation_handler


def test_citation_handler_writes(tmp_path):
    citation_file = tmp_path / "citations.json"

    def fake_add_citation(info, path):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump([info], f)

    with patch("utils.citation_handler.add_citation", side_effect=fake_add_citation) as mock_add:
        result = citation_handler("response", citation_info={"src": "doc"}, citation_path=citation_file)

    assert result == "response"
    assert citation_file.exists()
    with open(citation_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data == [{"src": "doc"}]
    citation_file.unlink()
    assert not citation_file.exists()
    mock_add.assert_called_once_with({"src": "doc"}, citation_file)
