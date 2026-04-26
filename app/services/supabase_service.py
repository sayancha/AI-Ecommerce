from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from supabase import Client, create_client

from app.config import get_settings


class SupabaseSalesService:
    def __init__(self) -> None:
        settings = get_settings()
        self.table_name = settings.supabase_sales_table
        self.client: Client = create_client(settings.supabase_url, settings.supabase_key)

    def fetch_sales_rows(self, limit: int = 500) -> list[dict[str, Any]]:
        response = (
            self.client.table(self.table_name)
            .select("*")
            .order("order_date", desc=True)
            .limit(limit)
            .execute()
        )
        return response.data or []

    @staticmethod
    def _safe_float(value: Any) -> float:
        if value is None:
            return 0.0
        return float(value)

    @staticmethod
    def _safe_int(value: Any) -> int:
        if value is None:
            return 0
        return int(value)

    def build_metrics(self, rows: list[dict[str, Any]]) -> dict[str, Any]:
        revenue = sum(self._safe_float(row.get("total_amount")) for row in rows)
        units = sum(self._safe_int(row.get("quantity")) for row in rows)
        avg_order_value = revenue / len(rows) if rows else 0

        by_region: dict[str, float] = {}
        by_product: dict[str, float] = {}
        by_status: dict[str, int] = {}

        for row in rows:
            region = str(row.get("region") or "Unknown")
            product = str(row.get("product_name") or "Unknown")
            status = str(row.get("status") or "Unknown")
            amount = self._safe_float(row.get("total_amount"))

            by_region[region] = by_region.get(region, 0) + amount
            by_product[product] = by_product.get(product, 0) + amount
            by_status[status] = by_status.get(status, 0) + 1

        top_region = max(by_region.items(), key=lambda item: item[1])[0] if by_region else "N/A"
        top_product = max(by_product.items(), key=lambda item: item[1])[0] if by_product else "N/A"

        return {
            "row_count": len(rows),
            "revenue": round(revenue, 2),
            "units": units,
            "avg_order_value": round(avg_order_value, 2),
            "by_region": by_region,
            "by_product": by_product,
            "by_status": by_status,
            "top_region": top_region,
            "top_product": top_product,
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }
