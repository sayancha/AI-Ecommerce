# AI Ecommerce Sales Chatbot

This project builds a multi-agent sales chatbot with:

- `FastAPI` backend API
- `Streamlit` chat UI
- `OpenRouter` LLM through `LangChain`
- `Supabase` for sales data
- `Gmail` for sending report emails
- `Faker` for generating demo sales data

## How it works

1. The user sends a question from the Streamlit UI.
2. FastAPI receives the message on `/chat`.
3. The LangChain routing agent decides whether to call:
   - the `SupabaseAgent` for analytics questions, or
   - the `GmailAgent` when the user asks to email a report.
4. The `SupabaseAgent` queries sales rows from Supabase and creates a business-friendly answer.
5. The `GmailAgent` reuses the sales insight, drafts a report, and sends it through Gmail SMTP.

## Project structure

```text
app/
  agents/
  services/
  config.py
  main.py
  schemas.py
scripts/
  seed_fake_sales.py
sql/
  sales_schema.sql
streamlit_app.py
requirements.txt
.env.example
```

## Environment variables

Copy `.env.example` to `.env` and fill in your real values.

```env
OPENROUTER_API_KEY=
OPENROUTER_MODEL=openai/gpt-4.1-mini
OPENROUTER_MAX_TOKENS=1200
SUPABASE_URL=
SUPABASE_KEY=
SUPABASE_SALES_TABLE=sales_records
GMAIL_SENDER_EMAIL=
GMAIL_APP_PASSWORD=
DEFAULT_REPORT_RECIPIENT=
FASTAPI_BASE_URL=http://127.0.0.1:8000
```

`OPENROUTER_MAX_TOKENS` caps the maximum model response size. Keep it modest on Railway/OpenRouter so each request does not reserve the model's full output window.

## Gmail setup

- Turn on 2-Step Verification for your Gmail account.
- Create a Gmail App Password.
- Put that 16-character password into `GMAIL_APP_PASSWORD`.

## Supabase setup

1. Create a Supabase project.
2. Open the SQL editor and run `sql/sales_schema.sql`.
3. Put your Supabase URL and API key in `.env`.
4. Seed demo sales data with the Faker script.

## Steps to run on localhost in VS Code

1. Open this folder in VS Code.
2. Install Python 3.12 if it is not already installed.
   Python 3.13 can fail on some Windows setups when pip tries to build native packages like `zstandard` or `cffi`.
3. Open the VS Code terminal in this folder.
4. Create a virtual environment:

```powershell
py -3.12 -m venv .venv
```

5. Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

6. Install dependencies:

```powershell
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

7. Create your env file:

```powershell
Copy-Item .env.example .env
```

8. Update `.env` with your OpenRouter, Supabase, and Gmail credentials.
9. Create the sales table in Supabase using `sql/sales_schema.sql`.
10. Seed demo data:

```powershell
python -m scripts.seed_fake_sales
```

11. Start the FastAPI backend:

```powershell
uvicorn app.main:app --reload
```

12. Open another VS Code terminal and start the Streamlit UI:

```powershell
streamlit run streamlit_app.py
```

13. Open the Streamlit URL shown in the terminal, usually `http://localhost:8501`.

## Example prompts

- `What is the total revenue from the latest sales data?`
- `Which region is performing best this month?`
- `Email the latest sales summary to finance@example.com`
- `Send a product-wise sales report to ceo@example.com`

## API example

```bash
curl -X POST http://127.0.0.1:8000/chat ^
  -H "Content-Type: application/json" ^
  -d "{\"message\":\"Email the latest sales report to finance@example.com\"}"
```

## Notes

- The router uses the LLM for intent routing between the two agents.
- For email requests, the Gmail agent first gets the sales insight, then sends it as an email.
- If you want stronger SQL-level filtering, you can extend the Supabase service with custom RPCs or Postgres functions.
