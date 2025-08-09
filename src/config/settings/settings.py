from src.config.settings.postgres import PostgresSettings
from src.config.settings.project import ProjectSettings


class Settings:
    PROJECT = ProjectSettings()
    POSTGRES = PostgresSettings()
