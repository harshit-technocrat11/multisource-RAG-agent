import streamlit as st

def render_chat(chat_history):

    st.markdown('<div class="chat-container">', unsafe_allow_html=True)

    for msg in chat_history:

        st.markdown(
            f'<div class="user-bubble">{msg["user"]}</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f'<div class="bot-bubble">{msg["bot"]}</div>',
            unsafe_allow_html=True
        )

    st.markdown('</div>', unsafe_allow_html=True)
