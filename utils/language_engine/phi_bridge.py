"""Bridge to a local Phi-3 model via HTTP."""

try:
    import requests  # type: ignore
except Exception:  # pragma: no cover - requests may be missing
    requests = None


def query_phi3(prompt: str) -> str:
    """Send ``prompt`` to a locally running Phi-3 server."""
    if requests is None:
        return "[phi3 unavailable]"
    payload = {
        "model": "phi3:mini-4k-instruct",
        "messages": [{"role": "user", "content": prompt}],
    }
    try:  # pragma: no cover - network call
        response = requests.post(
            "http://localhost:1234/v1/chat/completions",
            json=payload,
            timeout=10,
        )
        data = response.json()
        choices = data.get("choices") or []
        if choices:
            return choices[0].get("message", {}).get("content", "")
        return data.get("error", {}).get("message", "[phi3 empty]")
    except Exception as exc:  # pragma: no cover - request failure
        return f"[phi3 error: {exc}]"


__all__ = ["query_phi3"]
