"""Small helper around NLTK WordNet."""

try:  # pragma: no cover - optional dependency
    from nltk.corpus import wordnet  # type: ignore
except Exception:  # pragma: no cover - NLTK may not be installed
    wordnet = None  # type: ignore


def get_word_info(word: str):
    """Return WordNet info for ``word`` if NLTK is available."""
    if wordnet is None:
        return None

    synsets = wordnet.synsets(word)
    return {
        "definitions": [s.definition() for s in synsets],
        "examples": [ex for s in synsets for ex in s.examples()],
        "synonyms": list({lemma.name() for s in synsets for lemma in s.lemmas()}),
        "hypernyms": [h.name() for s in synsets for h in s.hypernyms()],
    }