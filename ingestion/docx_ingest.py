from docx import Document as DocxDocument
from langchain_core.documents import Document

def ingest_docx(path):

    doc = DocxDocument(path)

    text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())

    return [
        Document(
            page_content=text,
            metadata={"type": "docx", "source": path}
        )
    ]
