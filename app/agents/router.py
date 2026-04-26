from typing import Literal, Optional

from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from app.services.llm import build_llm


class RouteDecision(BaseModel):
    route: Literal["supabase", "gmail"] = Field(
        description="Choose gmail when the user wants an email/report sent, otherwise supabase."
    )
    recipient_email: Optional[str] = Field(
        default=None,
        description="Recipient email if the user explicitly mentions one.",
    )
    reason: str


class RouterAgent:
    def __init__(self) -> None:
        self.llm = build_llm(temperature=0)
        self.structured_llm = self.llm.with_structured_output(RouteDecision)
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You route sales assistant requests. "
                    "Choose 'gmail' only if the user wants an email sent or asks for a report to be mailed. "
                    "Choose 'supabase' for analytics, metrics, totals, trends, product or region insights.",
                ),
                ("human", "{message}"),
            ]
        )

    def decide(self, message: str) -> RouteDecision:
        chain = self.prompt | self.structured_llm
        return chain.invoke({"message": message})
