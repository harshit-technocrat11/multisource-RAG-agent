import fitz
import io
from PIL import Image
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from ingestion.image_ingest import ingest_image
# import image base64 helper
# from ingestion.image_utilities import image_to_base64
import base64, io 
vision_llm = ChatOpenAI(model="gpt-4o")

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1500,
    chunk_overlap=100
)

def ingest_pdf(path):

    doc = fitz.open(path)
    all_docs =[]

    for i, page in enumerate(doc):
        
        # TEXT
        text = page.get_text()
        if text.strip():
            base_doc = Document(
                page_content=text,
                metadata={"page": i, "type": "text", "source": path}
            )
            chunks = splitter.split_documents([base_doc])
            all_docs.extend(chunks)

        # IMAGES
        for img in page.get_images(full=True):

            xref = img[0]
            image_bytes = doc.extract_image(xref)["image"]

            docs_from_image = ingest_image(
            image_bytes,
            source=path
            )

    all_docs.extend(docs_from_image)


    doc.close()

    return all_docs