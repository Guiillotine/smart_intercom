from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class FaceSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf8",
        extra="allow"
    )

    FACE_PROVIDER: str = Field(default="CUDAExecutionProvider")

    DET_SCORE_THRESHOLD: float = Field(default=0.6)
