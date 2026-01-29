import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from rag.persistence import load_vectorstore
from rag.vectordb_embeddings import create_vectorstore
from rag.retriever import get_retriever

from ui.layout import setup_page, render_title
from ui.sidebar import render_sidebar
from ui.chat_interface import render_chat
from ui.inputbox import render_input

from handlers.ingestion_handler import handle_ingestion
from handlers.chat_handler import handle_chat


# --------------------
# Setup UI
# --------------------

setup_page()
render_title()


# --------------------
# Load DB if exists
# --------------------

if "retriever" not in st.session_state:

    existing_db = load_vectorstore()

    if existing_db:
        st.session_state.retriever = get_retriever(existing_db)
    else:
        st.session_state.retriever = None


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# --------------------
# Sidebar
# --------------------

uploaded_files, url, ingest_btn = render_sidebar()


# --------------------
# Ingestion
# --------------------

if ingest_btn:

    with st.spinner("Ingesting data..."):

        docs = handle_ingestion(uploaded_files, url)

        if docs:
            vectorstore = create_vectorstore(docs)
            st.session_state.retriever = get_retriever(vectorstore)
            st.success("✅ Data ingested!")
        else:
            st.warning("No data provided")


# --------------------
# Chat interface
# --------------------

render_chat(st.session_state.chat_history)


# --------------------
# Input
# --------------------

user_query, ask_btn = render_input()


# --------------------
# Chat logic
# --------------------

if ask_btn and user_query:

    if not st.session_state.retriever:
        st.warning("Please ingest data first!")

    else:
        with st.spinner("Thinking..."):

            answer = handle_chat(
                st.session_state.retriever,
                user_query
            )

        st.session_state.chat_history.append({
            "user": user_query,
            "bot": answer
        })

        st.rerun()
