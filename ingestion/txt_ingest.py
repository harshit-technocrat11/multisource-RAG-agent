from langchain_core.documents import Document 

def ingest_txt ( path):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    return [
        Document(
            page_content=text,
            metadata={"type": "txt", "source": path}
        )
    ]