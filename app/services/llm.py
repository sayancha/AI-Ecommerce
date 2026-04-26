from langchain_openai import ChatOpenAI

from app.config import get_settings


def build_llm(temperature: float = 0) -> ChatOpenAI:
    settings = get_settings()
    return ChatOpenAI(
        model=settings.openrouter_model,
        api_key=settings.openrouter_api_key,
        base_url="https://openrouter.ai/api/v1",
        temperature=temperature,
        default_headers={
            "HTTP-Referer": "http://localhost",
            "X-Title": "AI Ecommerce Chatbot",
        },
    )
