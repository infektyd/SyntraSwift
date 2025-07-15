import json
import os
import sys
from io import StringIO
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch, Mock
from importlib import reload

# Ensure repository root is on sys.path so 'utils' can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.modules.setdefault("spacy", Mock())
sys.modules.setdefault("openai", Mock())
sys.modules.setdefault("requests", Mock())
sys.modules.setdefault("utils.helper_functions", Mock())  # legacy shim

from utils.io_tools import load_config


def _import_language_core():
    """Import language_core with helper load_config patched."""
    with patch("utils.io_tools.load_config", return_value={}):
        import utils.language_engine.language_core as lc

        reload(lc)
    return lc


def test_run_language_loop_prints():
    lc = _import_language_core()
    cfg = {
        "enable_valon_output": True,
        "enable_modi_output": True,
        "enable_drift_output": True,
    }
    with patch.object(lc, "mistral_summarize", return_value="mistral"), patch.object(
        lc, "query_phi3", return_value="chat"
    ), patch.object(lc, "get_word_info", return_value={}), patch.object(
        lc, "analyze_structure", return_value={}
    ), patch.object(
        lc, "process_through_brains"
    ) as mock_process, patch.object(
        lc, "load_config", return_value=cfg
    ):
        mock_process.return_value = {"valon": "VAL", "modi": "MOD", "drift": "DRIFT"}
        buf = StringIO()
        with redirect_stdout(buf):
            result = lc.run_language_loop("hello")
    output = buf.getvalue()
    assert "[DEBUG]" not in output
    assert "VALON SAYS" in output
    assert "MODI SAYS" in output
    assert "SYNTRA DRIFT OUTPUT" in output
    assert result == "DRIFT"


def test_run_language_loop_suppresses():
    lc = _import_language_core()
    cfg = {
        "enable_valon_output": False,
        "enable_modi_output": False,
        "enable_drift_output": False,
    }
    with patch.object(lc, "mistral_summarize", return_value="mistral"), patch.object(
        lc, "query_phi3", return_value="chat"
    ), patch.object(lc, "get_word_info", return_value={}), patch.object(
        lc, "analyze_structure", return_value={}
    ), patch.object(
        lc, "process_through_brains"
    ) as mock_process, patch.object(
        lc, "load_config", return_value=cfg
    ):
        mock_process.return_value = {"valon": "VAL", "modi": "MOD", "drift": "DRIFT"}
        buf = StringIO()
        with redirect_stdout(buf):
            result = lc.run_language_loop("hello")
    output = buf.getvalue()
    assert "VALON SAYS" not in output
    assert "MODI SAYS" not in output
    assert "SYNTRA DRIFT OUTPUT" not in output
    assert result == "DRIFT"


def test_run_language_loop_debug_trace():
    lc = _import_language_core()
    cfg = {
        "enable_valon_output": True,
        "enable_modi_output": True,
        "enable_drift_output": True,
    }
    with patch.object(lc, "mistral_summarize", return_value="mistral"), patch.object(
        lc, "query_phi3", return_value="chat"
    ), patch.object(lc, "get_word_info", return_value={}), patch.object(
        lc, "analyze_structure", return_value={}
    ), patch.object(
        lc, "process_through_brains"
    ) as mock_process, patch.object(
        lc, "load_config", return_value=cfg
    ):
        mock_process.return_value = {"valon": "VAL", "modi": "MOD", "drift": "DRIFT"}
        buf = StringIO()
        with redirect_stdout(buf):
            result = lc.run_language_loop("hello", debug_output_trace=True)
    output = buf.getvalue()
    assert "[DEBUG] COGNITION TRACE" in output
    assert "VALON SAYS" in output
    assert "MODI SAYS" in output
    assert "SYNTRA DRIFT OUTPUT" in output
    assert result == "DRIFT"


def test_debug_trace_respects_config_flags():
    lc = _import_language_core()
    cfg = {
        "enable_valon_output": False,
        "enable_modi_output": False,
        "enable_drift_output": False,
    }
    with patch.object(lc, "mistral_summarize", return_value="mistral"), patch.object(
        lc, "query_phi3", return_value="chat"
    ), patch.object(lc, "get_word_info", return_value={}), patch.object(
        lc, "analyze_structure", return_value={}
    ), patch.object(
        lc, "process_through_brains"
    ) as mock_process, patch.object(
        lc, "load_config", return_value=cfg
    ):
        mock_process.return_value = {"valon": "VAL", "modi": "MOD", "drift": "DRIFT"}
        buf = StringIO()
        with redirect_stdout(buf):
            result = lc.run_language_loop("hello", debug_output_trace=True)
    output = buf.getvalue()
    assert "[DEBUG] COGNITION TRACE" in output
    assert "VALON SAYS" not in output
    assert "MODI SAYS" not in output
    assert "SYNTRA DRIFT OUTPUT" not in output
    assert result == "DRIFT"


def test_load_config_fallback(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("ELEVENLABS_API_KEY", raising=False)
    local_path = Path("config/config.local.json")
    if local_path.exists():
        local_path.rename(local_path.with_suffix(".bak"))
        restore = True
    else:
        restore = False
    try:
        cfg = load_config()
    finally:
        if restore:
            local_path.with_suffix(".bak").rename(local_path)
    with open("config.json", "r", encoding="utf-8") as f:
        default_cfg = json.load(f)
    assert cfg.get("openai_api_key") == default_cfg["openai_api_key"]
    assert cfg.get("enable_valon_output") == default_cfg["enable_valon_output"]


def test_get_word_info_no_nltk(monkeypatch):
    """wordnet_hook gracefully handles missing nltk dependency."""
    monkeypatch.setitem(sys.modules, "nltk", None)
    import importlib
    import utils.language_engine.wordnet_hook as wh

    importlib.reload(wh)

    assert wh.wordnet is None
    assert wh.get_word_info("dog") is None


def test_run_swift_error_logged(tmp_path, monkeypatch):
    """_run_swift returns an error string and logs when the subprocess fails."""
    import utils.reasoning_engine as re
    import subprocess

    monkeypatch.chdir(tmp_path)
    err = subprocess.CalledProcessError(1, ["swift"], stderr="boom")
    with patch("subprocess.run", side_effect=err):
        result = re._run_swift("reflect_valon", "test")

    assert result.startswith("ERROR: Swift command failed")
    log_file = tmp_path / "entropy_logs" / "run_swift_errors.json"
    assert log_file.exists()
    with open(log_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    entry = data[-1]
    assert entry["command"] == "reflect_valon"
    assert entry["args"] == ["test"]
    assert "boom" in entry["error"]
