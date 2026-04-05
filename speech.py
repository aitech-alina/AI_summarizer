import whisper

model = None


def _load_model():
    global model
    if model is None:
        model = whisper.load_model("base")

def speech_to_text(file_path):
    _load_model()
    result = model.transcribe(file_path)
    return result["text"]