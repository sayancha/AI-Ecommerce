import logging

from fastapi import FastAPI, HTTPException

from app.agents.gmail_agent import GmailAgent
from app.agents.router import RouterAgent
from app.agents.supabase_agent import SupabaseAgent
from app.schemas import ChatRequest, ChatResponse

app = FastAPI(title="AI Ecommerce Sales Chatbot", version="1.0.0")
logger = logging.getLogger(__name__)

router_agent = RouterAgent()
supabase_agent = SupabaseAgent()
gmail_agent = GmailAgent()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest) -> ChatResponse:
    try:
        decision = router_agent.decide(payload.message)
        if decision.route == "gmail":
            return gmail_agent.handle(payload.message, decision.recipient_email)

        insight = supabase_agent.analyze(payload.message)
        return ChatResponse(
            route="supabase",
            answer=insight.answer,
            report_preview=insight.report_body,
        )
    except Exception as exc:
        logger.exception("Chat request failed")
        raise HTTPException(status_code=500, detail=str(exc)) from exc
