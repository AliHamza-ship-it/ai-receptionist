from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    supabase_url: str
    supabase_secret_key: str

    retell_api_key: str
    retell_agent_id: str

    app_env: str = "development"
    business_timezone: str = "Asia/Karachi"

    model_config = SettingsConfigDict(
        env_file="../.env",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()