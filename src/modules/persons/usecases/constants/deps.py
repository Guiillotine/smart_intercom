from typing import Annotated

from fastapi import Depends

from src.modules.persons.constants import PersonEnums
from src.modules.persons.constants.deps import get_person_common_enums
from src.modules.persons.schemas.constants import PersonSchemaEnums
from src.modules.persons.schemas.constants.deps import get_person_schema_enums
from src.modules.persons.usecases.constants import EmployeeUCEnums


def get_employee_usecase_enums(
    person_common_enums: Annotated[PersonEnums, Depends(get_person_common_enums)],
    person_schema_enums: Annotated[PersonSchemaEnums, Depends(get_person_schema_enums)],
) -> EmployeeUCEnums:
    """
    Dependency provider for EmployeeUCEnums instance.

    :return: Initialized Employee usecase enums instance
    """
    return EmployeeUCEnums(
        person_common_enums=person_common_enums,
        person_schema_enums=person_schema_enums,
    )
