from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf8",
        extra="allow"
    )

    HOST: str = Field(default="localhost", alias="POSTGRES_HOST")
    PORT: int = Field(default=5432, alias="POSTGRES_PORT")
    DB: str = Field(default="example", alias="POSTGRES_DB")
    USER: str = Field(default="example", alias="POSTGRES_USER")
    PASSWORD: str = Field(default="example", alias="POSTGRES_PASSWORD")
    DIMENSION: str = Field(default=1536)
