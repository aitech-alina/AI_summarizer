import importlib
import re

_transformers = None
_pipeline = None


def _load_transformers():
    global _transformers
    if _transformers is not None:
        return _transformers

    try:
        _transformers = importlib.import_module("transformers")
    except Exception as e:
        print(f"Transformers import failed: {e}")
        _transformers = None
    return _transformers


def _get_summarizer():
    global _pipeline
    if _pipeline is not None:
        return _pipeline

    transformers = _load_transformers()
    if transformers is None:
        return None

    try:
        print("Loading summarization model...")
        from transformers import BartTokenizer, BartForConditionalGeneration
        tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")
        model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")
        _pipeline = {"tokenizer": tokenizer, "model": model}
        print("Summarization model loaded successfully")
    except Exception as e:
        print(f"Failed to load summarization model: {e}")
        _pipeline = None

    return _pipeline


def _naive_summary(text, max_sentences=3):
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    if len(sentences) <= max_sentences:
        return text.strip()
    return " ".join(sentences[:max_sentences]).strip()


def summarize_text(text):
    summarizer_instance = _get_summarizer()
    if summarizer_instance is not None and isinstance(summarizer_instance, dict):
        try:
            tokenizer = summarizer_instance["tokenizer"]
            model = summarizer_instance["model"]
            inputs = tokenizer(text, return_tensors="pt", max_length=1024, truncation=True)
            summary_ids = model.generate(inputs["input_ids"], max_length=150, min_length=50, length_penalty=2.0, num_beams=4, early_stopping=True)
            result = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            return result
        except Exception as e:
            print(f"Summarization failed: {e}")
    return _naive_summary(text)
