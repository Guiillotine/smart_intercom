from src.modules.persons.constants import PersonEnums


def get_person_common_enums() -> PersonEnums:
    """Dependency provider for PersonEnums instance.

    ## Returns:
    - EmployeeUCEnums: Initialized Person usecase enums instance
    """
    return PersonEnums()
