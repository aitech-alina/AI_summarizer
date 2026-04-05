from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

MODEL_NAME = "facebook/bart-large-cnn"
tokenizer = None
model = None


def _load_model():
    global tokenizer, model
    if tokenizer is None or model is None:
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

def summarize_text(text):
    _load_model()
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=1024)
    summary_ids = model.generate(
        inputs["input_ids"],
        attention_mask=inputs.get("attention_mask"),
        max_length=150,
        min_length=50,
        do_sample=False,
    )
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)