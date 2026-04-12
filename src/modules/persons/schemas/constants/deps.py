from src.modules.persons.schemas.constants import PersonSchemaEnums


def get_person_schema_enums() -> PersonSchemaEnums:
    """
    Return an instance of PersonEnums.

    :return: PersonSchemaEnums instance containing pydantic schema constants
    """
    return PersonSchemaEnums()
