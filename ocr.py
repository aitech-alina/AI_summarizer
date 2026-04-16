import importlib

TrOCRProcessor = None
VisionEncoderDecoderModel = None
Image = None
_processor = None
_ocr_model = None


def _load_ocr_modules():
    global TrOCRProcessor, VisionEncoderDecoderModel, Image
    if TrOCRProcessor is not None and VisionEncoderDecoderModel is not None and Image is not None:
        return TrOCRProcessor, VisionEncoderDecoderModel, Image

    try:
        transformers = importlib.import_module("transformers")
        TrOCRProcessor = getattr(transformers, "TrOCRProcessor", None)
        VisionEncoderDecoderModel = getattr(transformers, "VisionEncoderDecoderModel", None)
    except Exception as e:
        print(f"Transformers import failed: {e}")
        TrOCRProcessor = None
        VisionEncoderDecoderModel = None

    try:
        pil_image = importlib.import_module("PIL.Image")
        Image = getattr(pil_image, "Image", None)
    except Exception as e:
        print(f"PIL import failed: {e}")
        Image = None

    return TrOCRProcessor, VisionEncoderDecoderModel, Image


def _get_ocr_models():
    global _processor, _ocr_model
    if _processor is not None and _ocr_model is not None:
        return _processor, _ocr_model

    TrOCRProcessor_module, VisionEncoderDecoderModel_module, Image_module = _load_ocr_modules()
    if TrOCRProcessor_module is None or VisionEncoderDecoderModel_module is None or Image_module is None:
        return None, None

    try:
        print("Loading OCR models...")
        _processor = TrOCRProcessor_module.from_pretrained("microsoft/trocr-base-handwritten")
        _ocr_model = VisionEncoderDecoderModel_module.from_pretrained("microsoft/trocr-base-handwritten")
        print("OCR models loaded successfully")
    except Exception as e:
        print(f"Failed to load OCR models: {e}")
        _processor = None
        _ocr_model = None

    return _processor, _ocr_model


def image_to_text(image_path):
    processor, model = _get_ocr_models()
    if processor is None or model is None or Image is None:
        return "[OCR unavailable]"

    try:
        image = Image.open(image_path).convert("RGB")
        pixel_values = processor(images=image, return_tensors="pt").pixel_values
        generated_ids = model.generate(pixel_values)
        text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        return text
    except Exception as e:
        print(f"OCR processing failed: {e}")
        return "[OCR processing failed]"
