import spacy

nlp = spacy.load("en_core_web_sm")

def extract_keypoints(text):
    doc = nlp(text)
    keywords = list(set([token.text for token in doc if token.pos_ in ["NOUN", "PROPN"]]))
    return keywords[:20]