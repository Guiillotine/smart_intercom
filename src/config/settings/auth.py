from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AuthSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow",
    )

    TOKEN_SECRET_KEY: str = Field(default="secret_key", alias="TOKEN_SECRET_KEY")
    ALGORITHM: str = Field(default="HS256", alias="ALGORITHM")

    ACCESS_TOKEN_EXPIRE_SECONDS: int = 60 * 60
    REFRESH_TOKEN_EXPIRE_SECONDS: int = 60 * 60 * 24 * 30
