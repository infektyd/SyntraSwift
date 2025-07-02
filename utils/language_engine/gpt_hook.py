# language_engine/chatgpt_bridge.py
import openai

from utils.io_tools import load_config

_config = load_config()
openai.api.key = _config.get("openai_api_key", "lm-studio")
openai.api.base = _config.get("openai_api_base", "http://localhost:1234/v1")
DEFAULT_MODEL = _config.get("openai_model", "phi-3-mini-4k-instruct")

def query_chatgpt(prompt):
    response = openai.ChatCompletion.create(
        model=DEFAULT_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']
