from sqlalchemy.ext.asyncio import AsyncEngine

from src.client.storages.postgres.core import PostgresContextManager, \
    PostgresEngineProvider


def get_psql_context_manager() -> PostgresContextManager:
    return PostgresContextManager()

def get_psql_engine_provider() -> PostgresEngineProvider:
    return PostgresEngineProvider()
