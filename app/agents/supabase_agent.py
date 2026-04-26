from langchain_core.prompts import ChatPromptTemplate

from app.schemas import SalesInsight
from app.services.llm import build_llm
from app.services.supabase_service import SupabaseSalesService


class SupabaseAgent:
    def __init__(self) -> None:
        self.sales_service = SupabaseSalesService()
        self.llm = build_llm(temperature=0.2)
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a sales analytics assistant. Use the provided sales metrics and example rows only. "
                    "Answer clearly for business users. Also draft a concise email-ready report.",
                ),
                (
                    "human",
                    "User question:\n{question}\n\n"
                    "Aggregated metrics:\n{metrics}\n\n"
                    "Recent sample rows:\n{sample_rows}\n\n"
                    "Return a business answer, an email subject, and an email body in this format:\n"
                    "ANSWER:\n...\nSUBJECT:\n...\nBODY:\n...",
                ),
            ]
        )

    def analyze(self, question: str) -> SalesInsight:
        rows = self.sales_service.fetch_sales_rows()
        metrics = self.sales_service.build_metrics(rows)
        sample_rows = rows[:8]
        chain = self.prompt | self.llm
        response = chain.invoke(
            {
                "question": question,
                "metrics": metrics,
                "sample_rows": sample_rows,
            }
        ).content

        answer = self._extract_section(response, "ANSWER:", "SUBJECT:")
        subject = self._extract_section(response, "SUBJECT:", "BODY:")
        body = self._extract_section(response, "BODY:", None)

        return SalesInsight(
            answer=answer.strip(),
            report_subject=subject.strip(),
            report_body=body.strip(),
            row_count=metrics["row_count"],
        )

    @staticmethod
    def _extract_section(text: str, start_marker: str, end_marker: str | None) -> str:
        start = text.find(start_marker)
        if start == -1:
            return text.strip()
        start += len(start_marker)
        if end_marker is None:
            return text[start:]
        end = text.find(end_marker, start)
        if end == -1:
            return text[start:]
        return text[start:end]
