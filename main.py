from dotenv import load_dotenv
load_dotenv()
import os
from rag.vectordb_embeddings import create_vectorstore
from rag.retriever import get_retriever
from rag.chat_chain import answer_question

# contains all data - web , img ,  pdf ,...etx
all_docs=[]

from ingestion.pdf_ingest import ingest_pdf
from ingestion.image_ingest import ingest_image
from ingestion.web_ingest import ingest_web
from ingestion.txt_ingest import ingest_txt
from ingestion.csv_ingest import ingest_csv
from ingestion.docx_ingest import ingest_docx

from rag.vectordb_embeddings import create_vectorstore

all_docs = []

# pdf
all_docs += ingest_pdf(r"data/multimodal_sample.pdf")
# image
all_docs += ingest_image(r"data/taj-mahal-2949765_640.webp")
# website
all_docs += ingest_web("https://docs.langchain.com/oss/python/langchain/overview")
# txt
all_docs += ingest_txt(r"data/sample.txt")
# csv
all_docs += ingest_csv(r"data/MOCK_DATA.csv")
# docx
all_docs += ingest_docx(r"data/doc.docx")

vectorstore = create_vectorstore(all_docs)

# retriever
retriever = get_retriever(vectorstore)

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