from typing import Annotated

from fastapi import Depends

from src.client.storages.postgres.core import PostgresSessionContextManager, \
    PostgresEngineProvider
from src.config.settings import Settings
from src.config.settings.deps import get_settings


def get_psql_session_context_manager() -> PostgresSessionContextManager:
    return PostgresSessionContextManager()


def get_psql_engine_provider(
    settings: Annotated[Settings, Depends(get_settings)]
) -> PostgresEngineProvider:
    return PostgresEngineProvider(settings=settings)
