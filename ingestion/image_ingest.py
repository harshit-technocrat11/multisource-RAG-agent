import io, base64
from PIL import Image
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI
from ingestion.image_utilities import image_to_base64

vision_llm = ChatOpenAI(model="gpt-4o")

def ingest_image(file):

    pil_image = Image.open(file).convert("RGB")

    img_base64 = image_to_base64(pil_image)

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

    return [
        Document(
            page_content=caption,
            metadata={"type": "image", "source": "uploaded_image"}
        )
    ]
