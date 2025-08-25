from src.common.repositories.postgres import PostgresBaseRepo


def get_pg_base_repo() -> PostgresBaseRepo:
    return PostgresBaseRepo()
