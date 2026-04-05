from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil

from speech import speech_to_text
from summarizer import summarize_text
from keypoints import extract_keypoints
from ocr import image_to_text
from diagram import diagram_to_steps

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploads"

# Create uploads folder if not exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.get("/")
def home():
    return {"message": "AI Lecture Summarizer API Running 🚀"}


@app.post("/process")
async def process(file: UploadFile = File(...)):
    try:
        # Save file
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Detect file type
        filename = file.filename.lower()

        # 🔹 AUDIO FILES
        if filename.endswith((".mp3", ".wav", ".m4a")):
            text = speech_to_text(file_path)
            input_type = "audio"

        # 🔹 IMAGE FILES (Handwritten / Diagram)
        elif filename.endswith((".png", ".jpg", ".jpeg")):
            text = image_to_text(file_path)
            input_type = "image"

        # 🔹 TEXT FILES
        elif filename.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
            input_type = "text"

        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")

        # 🔹 SUMMARIZATION
        summary = summarize_text(text)

        # 🔹 KEY POINTS
        keypoints = extract_keypoints(text)

        # 🔹 BULLET POINTS (simple conversion)
        bullet_points = summary.split(". ")
        bullet_points = [point.strip() for point in bullet_points if point]

        # 🔹 DIAGRAM STEPS (only meaningful for image/text)
        diagram_steps = diagram_to_steps(text)

        return {
            "input_type": input_type,
            "extracted_text": text,
            "summary": summary,
            "keypoints": keypoints,
            "bullet_points": bullet_points,
            "diagram_steps": diagram_steps
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))