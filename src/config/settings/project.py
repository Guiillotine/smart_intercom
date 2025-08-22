from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ProjectSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf8",
        extra="allow"
    )

    PROJECT_NAME: str = "Smart Intercom"
    PROJECT_VERSION: str = "0.0.1"

    PORT: int = Field(default=8080)
    HOST: str = Field(default="localhost")
    SUPERUSER_LOGIN: str = Field(default="login")
    SUPERUSER_PASSW: str = Field(default="passw")
    DEBUG: bool = Field(default=True)
