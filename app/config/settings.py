from app.config.postgres import PostgresSettings
from app.config.project import ProjectSettings


class Settings:
    PROJECT = ProjectSettings()
    POSTGRES = PostgresSettings()


settings = Settings()
