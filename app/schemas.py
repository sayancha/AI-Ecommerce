from typing import Literal, Optional

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)


class SalesInsight(BaseModel):
    answer: str
    report_subject: str
    report_body: str
    row_count: int


class ChatResponse(BaseModel):
    route: Literal["supabase", "gmail"]
    answer: str
    email_sent: bool = False
    email_to: Optional[str] = None
    report_preview: Optional[str] = None
