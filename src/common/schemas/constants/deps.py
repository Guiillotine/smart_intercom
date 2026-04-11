from src.common.schemas.constants.enums import SchemaEnums


def get_schema_enums() -> SchemaEnums:
    """
    Return an instance of SchemaEnums.

    This function provides access to the MongoRepositoriesEnum, which contains
    predefined values for repository operations including
    supported operators and constants.

    :return: SchemaEnums instance containing pydantic schema constants
    """
    return SchemaEnums()
