from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from utils.pdf_reader import extract_text_from_pdf
from utils.text_chunker import chunk_text

import shutil
import os

app = FastAPI()

# Allow React frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Backend Running"}

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    upload_dir = "uploads"

    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    text = extract_text_from_pdf(file_path)
    chunks = chunk_text(text)

    return {
    "message": "PDF uploaded successfully",
    "filename": file.filename,
    "total_chunks": len(chunks),
    "chunks": chunks
}