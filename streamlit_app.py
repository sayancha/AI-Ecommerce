import requests
import streamlit as st
from dotenv import load_dotenv

from app.config import get_settings

load_dotenv()
settings = get_settings()


def post_chat_message(message: str) -> dict:
    response = requests.post(
        f"{settings.fastapi_base_url.rstrip('/')}/chat",
        json={"message": message},
        timeout=60,
    )
    try:
        response.raise_for_status()
    except requests.HTTPError as exc:
        error_message = f"Backend request failed with HTTP {response.status_code}."
        try:
            error_detail = response.json().get("detail")
        except ValueError:
            error_detail = response.text
        if error_detail:
            error_message = f"{error_message}\n\n{error_detail}"
        raise RuntimeError(error_message) from exc
    return response.json()

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
            try:
                data = post_chat_message(prompt)
                answer = data["answer"]
                if data.get("report_preview"):
                    answer += f"\n\nReport preview:\n\n{data['report_preview']}"
                st.markdown(answer)
            except (requests.RequestException, RuntimeError) as exc:
                answer = (
                    "I couldn't get a response from the backend. "
                    "Check the Railway logs and environment variables.\n\n"
                    f"Error: {exc}"
                )
                st.error(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
