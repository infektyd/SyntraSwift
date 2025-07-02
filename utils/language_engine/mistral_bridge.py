"""Lightweight bridge to a local Mistral/Ollama server."""

try:  # optional dependency
    import requests  # type: ignore
except Exception:  # pragma: no cover - requests may not be installed
    requests = None


def mistral_summarize(text: str) -> str:
    """Summarize ``text`` using a local Mistral server if available."""
    if requests is None:
        return "[Mistral unavailable]"
    try:  # pragma: no cover - network call
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "mistral", "prompt": f"Summarize: {text}", "stream": False},
            timeout=10,
        )
        return response.json().get("response", "[Mistral failed]")
    except Exception as exc:  # pragma: no cover - network or server error
        return f"[Mistral error: {exc}]"
