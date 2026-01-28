import base64, io 

from PIL import Image

def image_to_base64(pil_image):
    buffer = io.BytesIO()
    pil_image.save(buffer, format="PNG")
    return base64.b16encode(buffer.getvalue()).decode()