from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ASRSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf8",
        extra="allow"
    )

    ASR_MODEL_SIZE: str = Field(default="small")

    ASR_COMPUTE_TYPE: str = Field(default="int8")
