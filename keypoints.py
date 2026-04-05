import re
from collections import Counter

STOP_WORDS = {
    "a", "an", "the", "and", "or", "but", "if", "then", "else", "when", "while",
    "for", "to", "of", "in", "on", "at", "by", "with", "from", "as", "is", "are",
    "was", "were", "be", "been", "being", "it", "this", "that", "these", "those",
    "you", "we", "they", "he", "she", "i", "me", "my", "our", "your", "their",
    "can", "could", "should", "would", "may", "might", "will", "just", "not", "do",
    "does", "did", "done", "have", "has", "had", "also", "about", "into", "over",
    "under", "after", "before", "between", "through", "during", "without", "within",
}

def extract_keypoints(text):
    words = re.findall(r"[A-Za-z][A-Za-z0-9_'-]*", text.lower())
    filtered_words = [word for word in words if len(word) > 2 and word not in STOP_WORDS]
    most_common = Counter(filtered_words).most_common(20)
    return [word for word, _ in most_common]