import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if (OPENAI_API_KEY.startswith("sk-")):
    print("openai api key looks fine !")
else :
    print("openai api key - error")


from ingestion.pdf_ingest import ingest_pdf
from ingestion.image_ingest import ingest_image
from ingestion.web_ingest import ingest_web
from ingestion.txt_ingest import ingest_txt
from ingestion.csv_ingest import ingest_csv
from ingestion.docx_ingest import ingest_docx

from rag.vectordb_embeddings import create_vectorstore
from rag.retriever import get_retriever
from rag.chat_chain import answer_question_stream


# -------------------------
# Page config (mobile ready)
# -------------------------

st.set_page_config(
    page_title="Multimodal RAG Assistant",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------------
# Custom CSS (chat bubbles)
# -------------------------

st.markdown("""
<style>

.chat-container {
    max-width: 900px;
    margin: auto;
}

.user-bubble {
    background: #2b313e;
    color: white;
    padding: 12px 16px;
    border-radius: 14px;
    margin: 10px 0;
    text-align: right;
}

.bot-bubble {
    background: #f1f3f6;
    color: black;
    padding: 12px 16px;
    border-radius: 14px;
    margin: 10px 0;
    text-align: left;
}

.source-box {
    font-size: 0.85rem;
    color: #555;
    margin-top: 6px;
}

@media (max-width: 768px) {
    .chat-container {
        padding: 0 10px;
    }
}
</style>
""", unsafe_allow_html=True)


# -------------------------
# Title
# -------------------------

st.title("🤖 Multisource Multimodal RAG Assistant")


# -------------------------
# Sidebar (ingestion)
# -------------------------

with st.sidebar:
    st.header("📥 Upload Data")

    uploaded_files = st.file_uploader(
        "Drag & drop files",
        type=["pdf", "png", "jpg", "jpeg", "csv", "txt", "docx", "webp"],
        accept_multiple_files=True
    )

    url = st.text_input("Website URL")

    ingest_btn = st.button("🚀 Ingest Data")


# -------------------------
# Session state
# -------------------------

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "retriever" not in st.session_state:
    st.session_state.retriever = None


# -------------------------
# Ingestion logic
# -------------------------

if ingest_btn:

    all_docs = []

    with st.spinner("Ingesting data..."):

        for file in uploaded_files:

            name = file.name.lower()

            if name.endswith(".pdf"):
                all_docs += ingest_pdf(file)

            elif name.endswith((".png", ".jpg", ".jpeg", ".webp")):
                all_docs += ingest_image(file)

            elif name.endswith(".txt"):
                all_docs += ingest_txt(file)

            elif name.endswith(".csv"):
                all_docs += ingest_csv(file)

            elif name.endswith(".docx"):
                all_docs += ingest_docx(file)

        if url:
            all_docs += ingest_web(url)

        if all_docs:
            vectorstore = create_vectorstore(all_docs)
            st.session_state.retriever = get_retriever(vectorstore)

            st.success("✅ Data ingested successfully!")
        else:
            st.warning("⚠️ No data provided")


# -------------------------
# Chat display
# -------------------------

st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for msg in st.session_state.chat_history:

    st.markdown(
        f'<div class="user-bubble">{msg["user"]}</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="bot-bubble">{msg["bot"]}</div>',
        unsafe_allow_html=True
    )

st.markdown('</div>', unsafe_allow_html=True)


# -------------------------
# Input box (sticky feel)
# -------------------------

st.divider()

user_query = st.text_input(
    "Ask something...",
    placeholder="Type your question and press Enter"
)

ask_btn = st.button("Send")


# -------------------------
# Chat logic
# -------------------------

if ask_btn and user_query:

    if not st.session_state.retriever:
        st.warning("Please ingest data first!")

    else:
        with st.spinner("Thinking..."):

            stream, sources = answer_question_stream(
                st.session_state.retriever,
                user_query
            )

        # Create placeholder for streaming text
        bot_placeholder = st.empty()
        streamed_text = ""

        for chunk in stream:
            if chunk.content:
                streamed_text += chunk.content
                bot_placeholder.markdown(
                    f'<div class="bot-bubble">{streamed_text}</div>',
                    unsafe_allow_html=True
                )

        # Format sources cleanly
        unique_sources = {}

        for s in sources:
            src = s.metadata.get("source")
            loc = s.metadata.get("page", s.metadata.get("row", "N/A"))

            if src not in unique_sources:
                unique_sources[src] = set()

            unique_sources[src].add(loc)

        source_text = "\n".join(
            f"{src} (locations: {', '.join(map(str, locs))})"
            for src, locs in unique_sources.items()
        )

        final_answer = f"{streamed_text}\n\n📌 Sources:\n{source_text}"

        st.session_state.chat_history.append({
            "user": user_query,
            "bot": final_answer
        })

        st.rerun()

