"""Utilities for interacting with a local Mistral instance."""

import subprocess

try:  # optional dependency
    import requests  # type: ignore
except Exception:  # pragma: no cover - requests may not be installed
    requests = None

def query_mistral(prompt: str) -> str:
    """Query a local Mistral/Ollama server."""
    if requests is not None:
        try:  # pragma: no cover - network call
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": "mistral", "prompt": prompt, "stream": False},
                timeout=10,
            )
            return response.json().get("response", "[Mistral failed]")
        except Exception:
            pass

    try:
        result = subprocess.run(
            ["ollama", "run", "mistral"],
            input=prompt.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=60,
        )
        return result.stdout.decode("utf-8").strip()
    except Exception as e:
        return f"[MISTRAL_ERROR] {e}"


def mistral_summarize(text: str) -> str:
    """Summarize ``text`` using :func:`query_mistral`."""
    return query_mistral(f"Summarize: {text}")
