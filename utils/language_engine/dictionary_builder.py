
import json
from pathlib import Path

def load_glossary():
    glossary_path = Path("memory_vault/modi/symbolic_glossary.json")
    if glossary_path.exists():
        with open(glossary_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def load_parts_of_speech():
    pos_path = Path("memory_vault/modi/parts_of_speech.json")
    if pos_path.exists():
        with open(pos_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def get_term_definition(term):
    glossary = load_glossary()
    return glossary.get(term, "Definition not found.")
