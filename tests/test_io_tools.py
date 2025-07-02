import json
import os
from pathlib import Path

import pytest

from utils.io_tools import load_config


def write_json(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f)


def test_load_config_search_order(tmp_path, monkeypatch):
    """`config/config.local.json` overrides other configs."""
    write_json(tmp_path / "config.json", {"val": "base"})
    write_json(tmp_path / "config.local.json", {"val": "local"})
    write_json(tmp_path / "config" / "config.local.json", {"val": "nested"})

    monkeypatch.chdir(tmp_path)
    cfg = load_config("config.json")
    assert cfg["val"] == "nested"


def test_load_config_second_choice(tmp_path, monkeypatch):
    """Falls back to `config.local.json` when nested file is absent."""
    write_json(tmp_path / "config.json", {"val": "base"})
    write_json(tmp_path / "config.local.json", {"val": "local"})

    monkeypatch.chdir(tmp_path)
    cfg = load_config("config.json")
    assert cfg["val"] == "local"


def test_load_config_env_override(tmp_path, monkeypatch):
    """Environment variables override file contents."""
    write_json(tmp_path / "config.json", {"openai_api_key": "file"})
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("OPENAI_API_KEY", "env")
    cfg = load_config("config.json")
    assert cfg["openai_api_key"] == "env"
