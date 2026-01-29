import streamlit as st

def render_input():

    st.divider()

    user_query = st.text_input(
        "Ask something...",
        placeholder="Type your question"
    )

    ask_btn = st.button("Send")

    return user_query, ask_btn
