import random
import json
from pathlib import Path

GLOSSARY_PATH = Path("memory_vault/modi/symbolic_glossary.json")
POS_PATH = Path("memory_vault/modi/parts_of_speech.json")

def load_json(path):
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def build_sentence(glossary, pos_data):
    nouns = [word for word, role in pos_data.items() if role == "noun"]
    verbs = [word for word, role in pos_data.items() if role == "verb"]
    objects = [word for word in glossary if word not in nouns and word not in verbs]

    if not (nouns and verbs and objects):
        return "[SYNTRA] Insufficient vocabulary to construct sentence."

    subject = random.choice(nouns)
    verb = random.choice(verbs)
    obj = random.choice(objects)

    return f"The {subject} {verb}s the {obj}."

def generate_summary_response():
    glossary = load_json(GLOSSARY_PATH)
    pos_data = load_json(POS_PATH)
    sentence = build_sentence(glossary, pos_data)
    return sentence

if __name__ == "__main__":
    print("[SYNTRA Sentence Builder] Sample Output:")
    print(generate_summary_response())
