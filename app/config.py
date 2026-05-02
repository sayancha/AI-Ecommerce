from functools import lru_cache

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    openrouter_api_key: str = Field(alias="OPENROUTER_API_KEY")
    openrouter_model: str = Field(default="openai/gpt-4.1-mini", alias="OPENROUTER_MODEL")
    openrouter_max_tokens: int = Field(default=1200, gt=0, alias="OPENROUTER_MAX_TOKENS")
    supabase_url: str = Field(alias="SUPABASE_URL")
    supabase_key: str = Field(alias="SUPABASE_KEY")
    supabase_sales_table: str = Field(default="sales_records", alias="SUPABASE_SALES_TABLE")
    gmail_sender_email: str = Field(alias="GMAIL_SENDER_EMAIL")
    gmail_app_password: str = Field(alias="GMAIL_APP_PASSWORD")
    default_report_recipient: str = Field(alias="DEFAULT_REPORT_RECIPIENT")
    fastapi_base_url: str = Field(default="http://127.0.0.1:8000", alias="FASTAPI_BASE_URL")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
