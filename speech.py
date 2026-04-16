import whisper

model = None

def load_model():
    global model
    if model is None:
        print("Loading Whisper model...")
        model = whisper.load_model("base")  # use "tiny" if slow
        print("Whisper loaded ")
    return model


def speech_to_text(audio_path):
    try:
        model = load_model()
        result = model.transcribe(audio_path)
        return result["text"]
    except Exception as e:
        print(f"Speech-to-text failed: {e}")
        return "[Speech recognition failed]"
