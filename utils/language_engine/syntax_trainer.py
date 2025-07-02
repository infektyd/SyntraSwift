# language_engine/syntax_trainer.py
try:
    import spacy
except Exception:  # pragma: no cover - optional dependency may be absent
    spacy = None

if spacy is not None:
    try:
        nlp = spacy.load("en_core_web_sm")
    except Exception as e:  # Catch all exceptions to avoid blocking behavior
        print(
            f"Warning: spaCy model 'en_core_web_sm' could not be loaded ({e}). "
            "analyze_structure will return an empty list."
        )
        nlp = None
else:
    nlp = None


def analyze_structure(sentence):
    if nlp is None:
        return []
    doc = nlp(sentence)
    return [
        {
            "text": token.text,
            "pos": token.pos_,
            "dep": token.dep_,
            "head": token.head.text,
        }
        for token in doc
    ]

