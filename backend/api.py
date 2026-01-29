from fastapi import FastAPI, UploadFile, File, Form
from typing import List, Optional
import tempfile
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ingestion.pdf_ingest import ingest_pdf
from ingestion.image_ingest import ingest_image
from ingestion.web_ingest import ingest_web
from ingestion.txt_ingest import ingest_txt
from ingestion.csv_ingest import ingest_csv
from ingestion.docx_ingest import ingest_docx

from rag.vectordb_embeddings import create_vectorstore
from rag.retriever import get_retriever
from rag.persistence import load_vectorstore

from rag.chat_chain import answer_question_stream

app = FastAPI(title="Multimodal RAG Backend")
from fastapi.responses import StreamingResponse
import asyncio

# Load DB if exists
retriever = None

existing_db = load_vectorstore()
if existing_db:
    retriever = get_retriever(existing_db)

# ingestion
@app.post("/ingest")
async def ingest(
    files: Optional[List[UploadFile]] = File(None),
    url: Optional[str] = Form(None)
):

    global retriever
    all_docs = []

    if files:
        for file in files:

            suffix = os.path.splitext(file.filename)[1]

            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(await file.read())
                tmp_path = tmp.name

            name = file.filename.lower()

            if name.endswith(".pdf"):
                all_docs += ingest_pdf(tmp_path)

            elif name.endswith((".png",".jpg",".jpeg",".webp")):
                all_docs += ingest_image(tmp_path)

            elif name.endswith(".txt"):
                all_docs += ingest_txt(tmp_path)

            elif name.endswith(".csv"):
                all_docs += ingest_csv(tmp_path)

            elif name.endswith(".docx"):
                all_docs += ingest_docx(tmp_path)

            os.remove(tmp_path)

    if url:
        all_docs += ingest_web(url)

    if not all_docs:
        return {"status": "no data"}

    vectorstore = create_vectorstore(all_docs)
    retriever = get_retriever(vectorstore)

    return {"status": "success", "docs": len(all_docs)}


# CHAT ENDPOINT

@app.get("/ask_stream")
async def ask_stream(question: str):

    if not retriever:
        return {"error": "No data ingested yet"}

    stream, _ = answer_question_stream(retriever, question)

    async def token_generator():
        for chunk in stream:
            if chunk.content:
                yield chunk.content
                await asyncio.sleep(0)

    return StreamingResponse(
        token_generator(),
        media_type="text/plain"
    )

# references /sources

@app.get("/sources")
async def get_sources(question: str):

    if not retriever:
        return {"error": "No data ingested"}

    _, docs = answer_question_stream(retriever, question)

    refs = []

    for d in docs:
        refs.append({
            "source": d.metadata.get("source", "unknown"),
            "page": d.metadata.get("page", d.metadata.get("row", "N/A")),
            "type": d.metadata.get("type", "text")
        })

    return {"sources": refs}
