import fitz
import io
from PIL import Image
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter

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
            pil_image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

            # Skip tiny images (optimization)
            if pil_image.width < 150 or pil_image.height < 150:
                continue

            # modified - force convert to PNG bytes , for unsupp img formats
            pil_image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
            buffer = io.BytesIO()
            pil_image.save(buffer, format="PNG")
            clean_image_bytes = buffer.getvalue()

            img_base64 = base64.b64encode(clean_image_bytes).decode()


            response = vision_llm.invoke([
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Describe this image clearly for retrieval"},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{img_base64}"
                            }
                        }
                    ]
                }
            ])

            caption = response.content

            all_docs.append(
                Document(
                    page_content=caption,
                    metadata={"page": i, "type": "image", "source": path}
                )
            )

    doc.close()

    return all_docs