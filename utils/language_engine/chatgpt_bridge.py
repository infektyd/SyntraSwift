"""Bridge to OpenAI's ChatGPT with optional ElevenLabs speech."""

from utils.io_tools import load_config

try:  # optional OpenAI dependency
    import openai  # type: ignore
except Exception:  # pragma: no cover - OpenAI may be absent
    openai = None

try:  # optional ElevenLabs dependency
    from elevenlabs import generate, play, set_api_key  # type: ignore
    ELEVENLABS_AVAILABLE = True
except Exception:  # pragma: no cover - optional dependency may not load
    ELEVENLABS_AVAILABLE = False

    def generate(*_args, **_kwargs):
        return b""

    def play(*_args, **_kwargs):
        return None

    def set_api_key(*_args, **_kwargs):
        return None

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

def load_key() -> str | None:
    """Return the ElevenLabs API key from config."""
    return load_config().get("elevenlabs_api_key")

def speak_text(text: str, voice: str = "Rachel") -> None:
    """Speak ``text`` aloud using ElevenLabs if available."""
    if not ELEVENLABS_AVAILABLE:
        print("[SYNTRA] ElevenLabs unavailable; skipping speech synthesis")
        return

    set_api_key(load_key())
    audio = generate(text=text, voice=voice, model="eleven_monolingual_v1")
    play(audio)

__all__ = ["query_chatgpt", "speak_text", "load_key", "openai", "ELEVENLABS_AVAILABLE"]