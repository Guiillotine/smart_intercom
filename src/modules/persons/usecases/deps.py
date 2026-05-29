from typing import Annotated

from fastapi import Depends

from src.common.constants import ErrorCodesEnums
from src.common.constants.deps import get_error_codes_enums
from src.modules.faces.interfaces import IFaceAnalyzerSrv
from src.modules.faces.services.deps import get_face_analyzer_service
from src.modules.persons.interfaces import IEmployeeUC, IPersonSrv
from src.modules.persons.services.deps import get_employee_service
from src.modules.persons.usecases.constants import EmployeeUCEnums
from src.modules.persons.usecases.constants.deps import get_employee_usecase_enums
from src.modules.persons.usecases.employee import EmployeeUC


async def get_employee_usecase(
    enums: Annotated[EmployeeUCEnums, Depends(get_employee_usecase_enums)],
    error_codes: Annotated[ErrorCodesEnums, Depends(get_error_codes_enums)],
    employee_service: Annotated[IPersonSrv, Depends(get_employee_service)],
    face_analyzer_service: Annotated[
        IFaceAnalyzerSrv, Depends(get_face_analyzer_service)
    ],
) -> IEmployeeUC:
    """
    Dependency factory that provides a configured employee use case instance.
    """

    return EmployeeUC(
        enums=enums,
        errors=error_codes,
        employee_service=employee_service,
        face_analyzer_service=face_analyzer_service,
    )
