import requests
import streamlit as st
from dotenv import load_dotenv

from app.config import get_settings

load_dotenv()
settings = get_settings()

st.set_page_config(page_title="AI Ecommerce Sales Chatbot", page_icon=":speech_balloon:", layout="wide")
st.title("AI Ecommerce Sales Chatbot")
st.caption("Ask for sales insights from Supabase or request an emailed sales report through Gmail.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Example: Email the latest regional sales summary to finance@example.com")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = requests.post(
                f"{settings.fastapi_base_url}/chat",
                json={"message": prompt},
                timeout=60,
            )
            response.raise_for_status()
            data = response.json()

            answer = data["answer"]
            if data.get("report_preview"):
                answer += f"\n\nReport preview:\n\n{data['report_preview']}"
            st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
