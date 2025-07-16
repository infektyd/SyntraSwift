"""Utility helpers for configuration and filesystem operations."""

import json
import os
from pathlib import Path
from typing import Dict


def load_config(path: str = "config.json") -> Dict:
    """Load configuration from JSON files with environment overrides.

    Search order:
        1. ``config/config.local.json``
        2. ``config.local.json``
        3. The provided ``path`` (defaults to ``config.json``)

    Environment variables override matching keys so secrets can be
    supplied without committing them to version control.
    """
    search_paths = [
        Path("config/config.local.json"),
        Path("config.local.json"),
        Path(path),
    ]
    config_path = next((p for p in search_paths if p.exists()), Path(path))

    config: Dict = {}
    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
    overrides = {
        "OPENAI_API_KEY": "openai_api_key",
        "ELEVENLABS_API_KEY": "elevenlabs_api_key",
        "APPLE_LLM_API_KEY": "apple_llm_api_key",
        "APPLE_LLM_API_BASE": "apple_llm_api_base",
        "USE_APPLE_LLM": "use_apple_llm",
    }
    for env_key, cfg_key in overrides.items():
        if env_key in os.environ:
            config[cfg_key] = os.environ[env_key]
    return config
