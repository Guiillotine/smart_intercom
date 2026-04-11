from src.common.adapters.repositories.postgres.constants import SchemaNamesEnum


def table_args(schema: SchemaNamesEnum, comment: str | None = None) -> dict:
    """
    Generates table arguments dictionary for SQLAlchemy models.

    :param schema: Enum value representing the PostgreSQL schema name.
    :param comment: Optional comment describing the table. Defaults to
                    '<schema> module schema' if not provided.
    :return: Dictionary with 'schema' and 'comment' keys for table metadata.
    """

    comment = comment if comment else f"{schema.value} module schema"

    return { "schema": schema.value, "comment": comment}
