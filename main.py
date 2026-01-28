from dotenv import load_dotenv
load_dotenv()
import os
from ingestion.pdf_ingest import ingest_pdf
from rag.vectordb_embeddings import create_vectorstore
from rag.retriever import get_retriever
from rag.chat_chain import answer_question

docs = ingest_pdf(r"data/multimodal_sample.pdf")

vectoredb = create_vectorstore(docs)
retriever = get_retriever(vectoredb)

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

while True:
    q = input("\nAsk: ")
    if q.lower() == "exit":
        break

    answer, sources = answer_question(retriever, q)

    print("\nAnswer:", answer)
    print("\nSources:")
    for s in sources:
        print("-", s.metadata)