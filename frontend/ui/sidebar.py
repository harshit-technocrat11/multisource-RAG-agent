import streamlit as st

def render_sidebar():

    with st.sidebar:

        st.header("📥 Upload Data")

        uploaded_files = st.file_uploader(
            "Drag & drop files",
            type=["pdf","png","jpg","jpeg","csv","txt","docx","webp"],
            accept_multiple_files=True
        )

        url = st.text_input("Website URL")

        ingest_btn = st.button("🚀 Ingest Data")

    return uploaded_files, url, ingest_btn
