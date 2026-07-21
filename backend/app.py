from pydoc import text
from unittest import result

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

#from backend.utils import embeddings
from utils.llm import get_llm_response
from utils.embeddings import create_embeddings
from utils.pdf_reader import extract_text_from_pdf
from utils.text_chunker import chunk_text
from utils.vector_store import create_vector_store
from utils.vector_store import search_vector_store

import shutil
import os

app = FastAPI()
vector_store = None
chunks = []
class ChatRequest(BaseModel):
    question: str

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
    global vector_store
    global chunks
    upload_dir = "uploads"

    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)


    text = extract_text_from_pdf(file_path)
    chunks = chunk_text(text)
    embeddings = create_embeddings(chunks)
    vector_store = create_vector_store(embeddings)


    return {
    "message": "PDF uploaded successfully",
    "filename": file.filename,
    "total_chunks": len(chunks),
    "chunks": chunks,
    "relevant_chunks": [chunks[i] for i in result[0]],
}

@app.post("/chat")
def chat(request: ChatRequest):

    question = request.question

    query_embedding = create_embeddings([question])

    result = search_vector_store(vector_store, query_embedding)

    context = "\n\n".join([chunks[i] for i in result[0]])

    answer = get_llm_response(question, context)

    return {
    "answer": answer
}