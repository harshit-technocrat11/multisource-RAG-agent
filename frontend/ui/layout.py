import streamlit as st

def setup_page():

    st.set_page_config(
        page_title="Multimodal RAG Assistant",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

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

    @media (max-width: 768px) {
        .chat-container {
            padding: 0 10px;
        }
    }

    </style>
    """, unsafe_allow_html=True)


def render_title():
    st.title("🤖 Multisource Multimodal RAG Assistant")
