import requests 
from bs4 import BeautifulSoup
from langchain_core.documents import Document
from ingestion.chunker import chunk_docs

def ingest_web(url):

    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    # remove junk
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()

    text = soup.get_text(separator=" ", strip=True)

    docs = [
        Document(
            page_content=text,
            metadata={"type": "web", "source": url}
        )
    ]
    docs = chunk_docs(docs)
    return docs