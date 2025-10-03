from src.client.storages.postgres.init import PostgresInitializer


def get_postgres_initializer() -> PostgresInitializer:
    return PostgresInitializer()
