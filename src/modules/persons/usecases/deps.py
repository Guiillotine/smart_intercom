from typing import Annotated

from fastapi import Depends

from src.modules.persons.interfaces import IEmployeeUC, IPersonSrv
from src.modules.persons.services.deps import get_person_service
from src.modules.persons.usecases.employee import EmployeeUC


async def get_employee_usecase(
    person_service: Annotated[IPersonSrv, Depends(get_person_service)],
) -> IEmployeeUC:
    """
    Dependency factory that provides a configured employee use case instance.

    :param person_service: Service handling shared person records.
    :return: Initialized employee use case instance.
    """

    return EmployeeUC(person_service=person_service)
