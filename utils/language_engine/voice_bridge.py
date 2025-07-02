# voice_bridge.py

"""Tiny ElevenLabs bridge used by SYNTRA."""

# ElevenLabs support disabled
# try:
#     from elevenlabs import Voice, generate, play
#     ELEVEN_AVAILABLE = True
# except Exception:  # optional dependency may not load
#     ELEVEN_AVAILABLE = False
#
#     class Voice:  # type: ignore
#         def __init__(self, *_, **__):
#             pass
#
#     def generate(*args, **kwargs):
#         return b""
#
#     def play(*args, **kwargs):
#         return None
ELEVEN_AVAILABLE = False

# from utils.helper_functions import load_config
import json

# config = load_config()
# ELEVEN_API_KEY = config.get("elevenlabs_api_key")


def choose_voice(drift_metadata=None, override=None):
    """Select an ElevenLabs voice based on DRIFT weights."""
    if override:
        return override

    if drift_metadata:
        valon_weight = drift_metadata.get("valon_weight", 0.5)
        if valon_weight > 0.75:
            return "Bella"    # Creative / Valon
        elif valon_weight < 0.25:
            return "Antoni"   # Logical / Modi
        else:
            return "Rachel"   # Balanced / SYNTRA

    return None  # Let ElevenLabs pick automatically


def speak_text(text, drift_meta=None, override_voice=None):
    """No-op speech function; prints text instead of speaking it."""
    print(f"[VOICE OMITTED] {text}")
