import requests

BACKEND_URL = "http://localhost:8000"

def handle_chat_stream(query):

    response = requests.get(
        f"{BACKEND_URL}/ask_stream",
        params={"question": query},
        stream=True
    )

    for chunk in response.iter_content(chunk_size=1024, decode_unicode=True):
        if chunk:
            yield chunk

# sources
def fetch_sources(query):

    r = requests.get(
        f"{BACKEND_URL}/sources",
        params={"question": query}
    )

    return r.json().get("sources", [])
