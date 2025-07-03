"""Bridge utilities for querying an Apple LLM service."""

from __future__ import annotations

import os

from utils.io_tools import load_config

try:  # optional dependency
    import requests  # type: ignore
except Exception:  # pragma: no cover - requests may not be installed
    requests = None


def query_apple_llm(prompt: str, api_key: str | None = None, base_url: str | None = None) -> str:
    """Query an Apple LLM service and return the response text."""
    if requests is None:
        return "[apple llm unavailable]"

    cfg = load_config()
    api_key = api_key or os.environ.get("APPLE_LLM_API_KEY") or cfg.get("apple_llm_api_key")
    base_url = base_url or os.environ.get("APPLE_LLM_API_BASE") or cfg.get(
        "apple_llm_api_base", "http://localhost:1234"
    )

    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    payload = {"model": "apple", "messages": [{"role": "user", "content": prompt}]}
    try:  # pragma: no cover - network call
        response = requests.post(f"{base_url}/v1/chat/completions", json=payload, headers=headers, timeout=10)
        data = response.json()
        choices = data.get("choices") or []
        if choices:
            return choices[0].get("message", {}).get("content", "")
        return data.get("error", {}).get("message", "[apple llm empty]")
    except Exception as exc:  # pragma: no cover - request failure
        return f"[apple llm error: {exc}]"


__all__ = ["query_apple_llm"]
