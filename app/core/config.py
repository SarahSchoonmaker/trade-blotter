from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import List, Optional

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    database_url: str = Field(default="postgresql+asyncpg://postgres:postgres@localhost:5432/trading", alias="DATABASE_URL")
    symbols: List[str] = Field(default_factory=lambda: ["AAPL", "MSFT", "ES"], alias="SYMBOLS")
    initial_prices: Optional[List[float]] = Field(default=None, alias="INITIAL_PRICES")
    tick_ms: int = Field(default=500, alias="TICK_MS")
    alpha_vantage_key: str = Field(default="", alias="ALPHA_VANTAGE_KEY")


settings = Settings()
