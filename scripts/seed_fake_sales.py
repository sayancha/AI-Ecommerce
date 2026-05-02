from __future__ import annotations

import random
import os
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from faker import Faker
from supabase import create_client

load_dotenv()
fake = Faker()


def required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def build_sales_rows(count: int = 100) -> list[dict]:
    products = [
        ("Wireless Mouse", "Accessories"),
        ("Mechanical Keyboard", "Accessories"),
        ("4K Monitor", "Displays"),
        ("USB-C Dock", "Accessories"),
        ("Gaming Laptop", "Computers"),
        ("Noise Cancelling Headphones", "Audio"),
    ]
    statuses = ["completed", "pending", "shipped", "returned"]
    regions = ["North", "South", "East", "West"]
    reps = ["Ava", "Liam", "Noah", "Emma", "Mia"]

    rows = []
    for _ in range(count):
        product_name, category = random.choice(products)
        quantity = random.randint(1, 5)
        unit_price = round(random.uniform(25, 1500), 2)
        order_date = datetime.now(timezone.utc) - timedelta(days=random.randint(0, 45))
        rows.append(
            {
                "order_id": fake.unique.bothify(text="ORD-#####"),
                "customer_name": fake.name(),
                "customer_email": fake.email(),
                "product_name": product_name,
                "category": category,
                "quantity": quantity,
                "unit_price": unit_price,
                "total_amount": round(quantity * unit_price, 2),
                "order_date": order_date.isoformat(),
                "region": random.choice(regions),
                "sales_rep": random.choice(reps),
                "status": random.choice(statuses),
            }
        )
    return rows


def main() -> None:
    supabase_url = required_env("SUPABASE_URL")
    supabase_key = required_env("SUPABASE_KEY")
    table_name = os.getenv("SUPABASE_SALES_TABLE", "sales_records")

    client = create_client(supabase_url, supabase_key)
    rows = build_sales_rows(120)
    client.table(table_name).insert(rows).execute()
    print(f"Inserted {len(rows)} fake sales rows into {table_name}.")


if __name__ == "__main__":
    main()
