from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class S3Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="allow"
    )

    ACCESS_KEY: str = Field(default="default_access_key", alias="S3_ACCESS_KEY")
    SECRET_KEY: str = Field(default="default_secret_key", alias="S3_SECRET_KEY")
    ENDPOINT_URL: str = Field(default="default_url", alias="S3_ENDPOINT_URL")
    REGION_NAME: str = Field(default="default_region_name", alias="S3_REGION_NAME")
    VISIT_BUCKET_NAME: str = Field(default="visit", alias="S3_VISIT_BUCKET_NAME")
    PERSON_BUCKET_NAME: str = Field(default="person", alias="S3_PERSON_BUCKET_NAME")
    MESSAGE_BUCKET_NAME: str = Field(default="message", alias="S3_MESSAGE_BUCKET_NAME")
