import pandas as pd
from langchain_core.documents import Document
from ingestion.chunker import chunk_docs

def ingest_csv(path):
    df = pd.read_csv(path)

    rows=[]

    for i, row in df.iterrows():
        row_text = ", ".join(f"{col}: {val}" for col, val in row.items())

        rows.append(
            Document(
                page_content=row_text,
                metadata={
                    "type": "csv",
                    "row": i,
                    "source": path
                }
            )
        )
    docs = chunk_docs(rows)

    return docs