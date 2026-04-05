from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image

MODEL_NAME = "microsoft/trocr-base-handwritten"
processor = None
model = None


def _load_model():
    global processor, model
    if processor is None or model is None:
        processor = TrOCRProcessor.from_pretrained(MODEL_NAME)
        model = VisionEncoderDecoderModel.from_pretrained(MODEL_NAME)

def image_to_text(image_path):
    _load_model()
    image = Image.open(image_path).convert("RGB")
    pixel_values = processor(images=image, return_tensors="pt").pixel_values
    generated_ids = model.generate(pixel_values)
    text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return text