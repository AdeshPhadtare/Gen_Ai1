import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# ----------------- LOAD ENV -----------------
load_dotenv()  # this will read your .env file
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("⚠️ No API key found. Please set GEMINI_API_KEY in .env file.")
else:
    genai.configure(api_key=API_KEY)

    st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖")

    model = genai.GenerativeModel("gemini-1.5-flash")

    # ----------------- MAIN APP -----------------
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Type your message..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            response = model.generate_content(prompt)
            bot_reply = response.text
        except Exception as e:
            bot_reply = f"⚠️ Error: {e}"

        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        with st.chat_message("assistant"):
            st.markdown(bot_reply)
