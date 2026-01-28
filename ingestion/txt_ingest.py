from langchain_core.documents import Document 
from ingestion.chunker import chunk_docs

def ingest_txt ( path):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    docs = [
        Document(
            page_content=text,
            metadata={"type": "txt", "source": path}
        )
    ]
    docs = chunk_docs(docs)
    return docs