from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class RuntimeSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf8",
        extra="allow"
    )

    DEVICE: str = Field(default="cpu")
