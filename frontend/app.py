import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from ui.layout import setup_page, render_title
from ui.sidebar import render_sidebar
from ui.chat_interface import render_chat
from ui.inputbox import render_input

from handlers.ingestion_handler import handle_ingestion
from handlers.chat_handler import handle_chat_stream, fetch_sources

from voice.tts import speak



# Setup UI


setup_page()
render_title()



# Session state

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# Sidebar

uploaded_files, url, ingest_btn = render_sidebar()


# Ingestion


if ingest_btn:

    with st.spinner("Ingesting data..."):

        res = handle_ingestion(uploaded_files, url)

        if res.get("status") == "success":
            st.success("✅ Data ingested into backend!")
        else:
            st.warning("⚠️ No data provided")



# Chat interface
render_chat(st.session_state.chat_history)


# Input
user_query, ask_btn = render_input()
use_voice = st.checkbox("🔊 Voice response")


# Chat logic
if ask_btn and user_query:

    bot_placeholder = st.empty()
    streamed_text = ""

    for token in handle_chat_stream(user_query):
        streamed_text += token
        formatted_text = streamed_text.replace("\n", "<br>")
        bot_placeholder.markdown(
            f'<div class="bot-bubble">{streamed_text}</div>',
            unsafe_allow_html=True
        )

    sources = fetch_sources(user_query)

    ref_text = "<br><br><b>📌 Sources:</b><br>"

    for s in sources:
        ref_text += f"• {s['source']} — {s['type']}, page- {s['page']}<br>"

    final_output = formatted_text + ref_text

    st.session_state.chat_history.append({
        "user": user_query,
        "bot": final_output
    })
    if use_voice:
        speak(streamed_text)

    st.rerun()
