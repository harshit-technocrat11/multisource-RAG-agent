from ingestion.pdf_ingest import ingest_pdf
from ingestion.image_ingest import ingest_image
from ingestion.web_ingest import ingest_web
from ingestion.txt_ingest import ingest_txt
from ingestion.csv_ingest import ingest_csv
from ingestion.docx_ingest import ingest_docx

def handle_ingestion(uploaded_files, url):

    all_docs = []

    for file in uploaded_files:

        name = file.name.lower()

        if name.endswith(".pdf"):
            all_docs += ingest_pdf(file)

        elif name.endswith((".png",".jpg",".jpeg",".webp")):
            all_docs += ingest_image(file)

        elif name.endswith(".txt"):
            all_docs += ingest_txt(file)

        elif name.endswith(".csv"):
            all_docs += ingest_csv(file)

        elif name.endswith(".docx"):
            all_docs += ingest_docx(file)

    if url:
        all_docs += ingest_web(url)

    return all_docs
