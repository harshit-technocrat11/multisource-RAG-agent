import requests

BACKEND_URL = "http://localhost:8000"

def handle_ingestion(uploaded_files, url):

    files_payload = []

    for file in uploaded_files:
        files_payload.append(
            ("files", (file.name, file.getvalue()))
        )

    data = {}
    if url:
        data["url"] = url

    r = requests.post(
        f"{BACKEND_URL}/ingest",
        files=files_payload if files_payload else None,
        data=data
    )

    return r.json()
