import io, base64
from PIL import Image
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI
from ingestion.chunker import chunk_docs

vision_llm = ChatOpenAI(model="gpt-4o")

# normalize --> allowing any type of img file   .png .jpg, .webp ...
def normalize_image(image_bytes_or_file):
    """
    Accepts:
    - raw bytes (from PDF)
    - file-like object (upload)

    Returns:
    - base64 PNG string
    """

    if isinstance(image_bytes_or_file, bytes):
        pil_image = Image.open(io.BytesIO(image_bytes_or_file))
    else:
        pil_image = Image.open(image_bytes_or_file)

    pil_image = pil_image.convert("RGB")

    buffer = io.BytesIO()
    pil_image.save(buffer, format="PNG")

    return base64.b64encode(buffer.getvalue()).decode()


def ingest_image(image_input, source="uploaded_image"):

    img_base64 = normalize_image(image_input)

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

    docs = [
        Document(
            page_content=caption,
            metadata={
                "type": "image",
                "source": source
            }
        )
    ]

    docs = chunk_docs(docs)
    return docs
