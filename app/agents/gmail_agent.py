import re

from app.config import get_settings
from app.schemas import ChatResponse
from app.services.gmail_service import GmailService
from app.agents.supabase_agent import SupabaseAgent


class GmailAgent:
    def __init__(self) -> None:
        self.gmail_service = GmailService()
        self.supabase_agent = SupabaseAgent()
        self.default_recipient = get_settings().default_report_recipient

    def handle(self, question: str, recipient_email: str | None = None) -> ChatResponse:
        insight = self.supabase_agent.analyze(question)
        to_email = recipient_email or self._extract_email(question) or self.default_recipient
        self.gmail_service.send_email(
            recipient=to_email,
            subject=insight.report_subject,
            body=insight.report_body,
        )
        return ChatResponse(
            route="gmail",
            answer=f"{insight.answer}\n\nThe report has been emailed to {to_email}.",
            email_sent=True,
            email_to=to_email,
            report_preview=insight.report_body,
        )

    @staticmethod
    def _extract_email(text: str) -> str | None:
        match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", text)
        return match.group(0) if match else None
