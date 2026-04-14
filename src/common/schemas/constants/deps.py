from src.common.schemas.constants.enums import SchemaEnums


def get_schema_enums() -> SchemaEnums:
    """
    Return an instance of SchemaEnums.

    :return: SchemaEnums instance containing pydantic schema constants
    """
    return SchemaEnums()
