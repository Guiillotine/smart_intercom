from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class BotSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf8",
        extra="allow"
    )

    BASE_URL: str = Field(default="https://api.vsegpt.ru/v1")

    MODEL: str = Field(default="openai/gpt-4o-mini")

    MODEL_SUPPORTS_STRUCTURED_OUTPUTS: bool = Field(default=False)

    API_KEY: str = Field(default="api_key")
