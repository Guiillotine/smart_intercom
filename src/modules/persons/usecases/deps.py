from typing import Annotated

from fastapi import Depends

from src.modules.persons.interfaces import IEmployeeUC, IPersonSrv
from src.modules.persons.services.deps import get_person_service
from src.modules.persons.usecases.constants import EmployeeUCEnums
from src.modules.persons.usecases.constants.deps import get_employee_usecase_enums
from src.modules.persons.usecases.employee import EmployeeUC


async def get_employee_usecase(
    enums: Annotated[EmployeeUCEnums, Depends(get_employee_usecase_enums)],
    employee_service: Annotated[IPersonSrv, Depends(get_person_service)],
) -> IEmployeeUC:
    """
    Dependency factory that provides a configured employee use case instance.

    :param enums: Enums for employee usecase layer.
    :param employee_service: Service handling shared employee records.
    :return: Initialized employee use case instance.
    """

    return EmployeeUC(
        enums=enums,
        employee_service=employee_service,
    )
