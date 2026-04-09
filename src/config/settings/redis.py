from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow",
    )

    HOST: str = Field(default="localhost", alias="REDIS_HOST")
    PORT: int = Field(default=6379, alias="REDIS_PORT")
