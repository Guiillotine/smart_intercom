from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


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
    DIMENSION: int = Field(default=1536)

    def get_url(self, use_async_driver: bool = False) -> str:
        driver = "asyncpg" if use_async_driver else "psycopg2"

        url = URL.create(
            drivername=f"postgresql+{driver}",
            username=self.USER,
            password=self.PASSWORD,
            host=self.HOST,
            port=self.PORT,
            database=self.DB,
        )

        return url.render_as_string(hide_password=False)

    @property
    def async_url(self) -> str:
        return self.get_url(use_async_driver=True)

    @property
    def sync_url(self) -> str:
        return self.get_url(use_async_driver=False)
