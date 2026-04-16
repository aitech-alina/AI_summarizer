from speech import speech_to_text
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

from summarizer import summarize_text
from keypoints import extract_keypoints
from ocr import image_to_text

from docx import Document
from PyPDF2 import PdfReader

app = FastAPI()

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.get("/")
def home():
    return {"message": "Backend is running"}


@app.get("/favicon.ico")
def favicon():
    from fastapi.responses import Response
    return Response(status_code=204)


@app.post("/process")
async def process_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = ""
    filename = file.filename.lower()

    # 🖼️ IMAGE → OCR
    if filename.endswith((".png", ".jpg", ".jpeg")):
        text = image_to_text(file_path)

    # 🎤 AUDIO → Whisper
    elif filename.endswith((".mp3", ".wav", ".m4a")):
        text = speech_to_text(file_path)

    # 📘 PDF
    elif filename.endswith(".pdf"):
        try:
            reader = PdfReader(file_path)
            for page in reader.pages:
                text += page.extract_text() or ""
        except Exception as e:
            print("PDF Error:", e)
            return {"error": "PDF processing failed ❌"}

    # 📝 WORD (.docx)
    elif filename.endswith(".docx"):
        try:
            doc = Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs])
        except Exception as e:
            print("DOCX Error:", e)
            return {"error": "Word file processing failed ❌"}

    # 📄 TEXT
    elif filename.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()

    else:
        return {"error": "Unsupported file format ❌"}

    # ⚠️ Safety check (VERY IMPORTANT)
    if not text or len(text.strip()) < 20:
        return {"error": "Could not extract meaningful text ❌"}

    # 🧠 AI Processing
    summary = summarize_text(text)
    keypoints = extract_keypoints(text)

    return {
        "summary": summary,
        "keypoints": keypoints
    }
