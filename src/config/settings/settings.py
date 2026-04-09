from src.config.settings.asr import ASRSettings
from src.config.settings.bot import BotSettings
from src.config.settings.face import FaceSettings
from src.config.settings.postgres import PostgresSettings
from src.config.settings.project import ProjectSettings
from src.config.settings.redis import RedisSettings
from src.config.settings.runtime import RuntimeSettings
from src.config.settings.s3 import S3Settings
from src.config.settings.tts import TTSSettings


class Settings:
    project = ProjectSettings()
    runtime = RuntimeSettings()
    s3 = S3Settings()
    redis = RedisSettings()
    postgres = PostgresSettings()
    face = FaceSettings()
    tts = TTSSettings()
    asr = ASRSettings()
    bot = BotSettings()
