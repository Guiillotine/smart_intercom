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

    SUPERUSER_EMAIL: str = Field(
        default="superuser@example.com", alias="SUPERUSER_LOGIN",
    )
    SUPERUSER_PASSWORD: str = Field(default="Superuser_123", alias="SUPERUSER_PASSW")
    SUPERUSER_FIRST_NAME: str = Field(default="System", alias="SUPERUSER_FIRST_NAME")
    SUPERUSER_LAST_NAME: str = Field(default="Administrator", alias="SUPERUSER_LAST_NAME")
