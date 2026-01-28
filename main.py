from dotenv import load_dotenv
load_dotenv()
import os
from ingestion.pdf_ingest import ingest_pdf
from rag.vectordb_embeddings import create_vectorstore
from rag.retriever import get_retriever
from rag.chat_chain import answer_question
from ingestion.image_ingest import ingest_image

# contains all data - web , img ,  pdf ,...etx
all_docs=[]

# pdf
pdf_docs = ingest_pdf(r"data/multimodal_sample.pdf")
all_docs.extend(pdf_docs)

# images
image_docs = ingest_image(r"data/taj-mahal-2949765_640.webp")
all_docs.extend(image_docs)


# vector store
vectoredb = create_vectorstore(all_docs)
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