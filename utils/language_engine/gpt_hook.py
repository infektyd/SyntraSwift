# language_engine/chatgpt_bridge.py
try:  # optional OpenAI dependency
    import openai  # type: ignore
except Exception:  # pragma: no cover - OpenAI may be absent
    openai = None

from utils.io_tools import load_config

_config = load_config()
if openai is not None:
    openai.api_key = _config.get("openai_api_key", "lm-studio")
    openai.api_base = _config.get("openai_api_base", "http://localhost:1234/v1")
    DEFAULT_MODEL = _config.get("openai_model", "phi-3-mini-4k-instruct")
else:
    DEFAULT_MODEL = "phi-3-mini-4k-instruct"

def query_chatgpt(prompt: str) -> str:
    """Send ``prompt`` to ChatGPT using the configured API key."""
    if openai is None:
        return "[ERROR: openai module not available]"
    try:  # pragma: no cover - network or API errors
        response = openai.ChatCompletion.create(
            model=DEFAULT_MODEL,
            messages=[{"role": "user", "content": prompt}],
        )
        return response["choices"][0]["message"]["content"]
    except Exception as exc:
        return f"[ERROR: {exc}]"

