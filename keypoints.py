import importlib
import re

spacy = None
_nlp = None
STOPWORDS = {
    "the", "and", "for", "with", "that", "this", "from", "they", "their",
    "have", "has", "are", "was", "were", "what", "when", "where",
    "which", "while", "there", "about", "between", "under", "over",
    "through", "because", "before", "after", "about", "also", "using",
    "use", "used", "can", "will", "would", "could",
}


def _load_spacy():
    global spacy
    if spacy is not None:
        return spacy

    try:
        spacy = importlib.import_module("spacy")
    except Exception as e:
        print(f"spaCy import failed: {e}")
        spacy = None
    return spacy


def _get_nlp():
    global _nlp
    if _nlp is not None:
        return _nlp

    spacy_module = _load_spacy()
    if spacy_module is None:
        return None

    try:
        print("Loading spaCy model...")
        _nlp = spacy_module.load("en_core_web_sm")
        print("spaCy model loaded successfully")
    except Exception as e:
        print(f"Failed to load spaCy model: {e}")
        _nlp = None

    return _nlp


def _naive_keypoints(text, max_keywords=20):
    words = re.findall(r"\b[a-zA-Z]{4,}\b", text.lower())
    freq = {}
    for word in words:
        if word in STOPWORDS:
            continue
        freq[word] = freq.get(word, 0) + 1
    return sorted(freq, key=freq.get, reverse=True)[:max_keywords]


def extract_keypoints(text):
    nlp_instance = _get_nlp()
    if nlp_instance is not None:
        try:
            doc = nlp_instance(text)
            keywords = list({token.text for token in doc if token.pos_ in ["NOUN", "PROPN"]})
            return keywords[:20]
        except Exception as e:
            print(f"spaCy extraction failed: {e}")
    return _naive_keypoints(text)
