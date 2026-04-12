from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends

from src.common.schemas import Msg, Pagination, PaginationResult
from src.modules.persons.controllers.constants import EmployeeCtrlEnums
from src.modules.persons.interfaces import IEmployeeCtrl
from src.modules.persons.interfaces.usecases import IEmployeeUC
from src.modules.persons.schemas import EmployeeCreate, Employee, EmployeeUpdate
from src.modules.persons.usecases.deps import get_employee_usecase


class EmployeeCtrl(IEmployeeCtrl):
    """
    Controller class for registering employee-related API endpoints.

    Employee endpoints operate on the shared persons module and expose only employee
    records through the employee use case.
    """

    def __init__(
        self,
        enums: EmployeeCtrlEnums,
    ):
        """
        Initializes the EmployeeCtrl and sets up routes.
        """

        self._controller = APIRouter()
        self._enums = enums
        self._add_controllers()

    @property
    def controller(self) -> APIRouter:
        """
        Exposes the FastAPI APIRouter instance containing registered routes.

        :return: The APIRouter with employee-related routes.
        """

        return self._controller

    def _add_controllers(self) -> None:
        """
        Registers API routes for employee management operations.
        """

        self._controller.add_api_route(
            path="",
            endpoint=self._enums.EmployeeCtrlPath.get_employee_list,
            methods=[self._enums.Common.RequestType.GET],
            response_model=PaginationResult[Employee],
        )
        self._controller.add_api_route(
            path=self._enums.EmployeeCtrlPath.create_employee,
            endpoint=self.create_employee,
            methods=[self._enums.Common.RequestType.POST],
            response_model=Employee,
        )
        self._controller.add_api_route(
            path=self._enums.EmployeeCtrlPath.update_employee,
            endpoint=self.update_employee,
            methods=[self._enums.Common.RequestType.PUT],
            response_model=Employee,
        )
        self._controller.add_api_route(
            path=self._enums.EmployeeCtrlPath.delete_employee,
            endpoint=self.delete_employee,
            methods=[self._enums.Common.RequestType.DELETE],
            response_model=Msg,
        )

    @staticmethod
    async def get_all_employees(
        pagination_params: Annotated[Pagination, Depends(Pagination)],
        employee_usecase: Annotated[IEmployeeUC, Depends(get_employee_usecase)],
    ) -> PaginationResult[Employee]:
        """
        Retrieve a paginated list of employee person records.

        :param pagination_params: Pagination settings.
        :param employee_usecase: Use case instance handling employee logic.
        :return: Paginated list of employees.
        """

        return await employee_usecase.get_all(pagination_params=pagination_params)

    @staticmethod
    async def create_employee(
        employee_in: EmployeeCreate,
        employee_usecase: Annotated[IEmployeeUC, Depends(get_employee_usecase)],
    ) -> Employee:
        """
        Create an employee person record.

        :param employee_in: Employee data from request body.
        :param employee_usecase: Use case instance handling employee logic.
        :return: Created employee data.
        """

        return await employee_usecase.create(employee_in=employee_in)

    @staticmethod
    async def update_employee(
        sid: UUID,
        employee_in: EmployeeUpdate,
        employee_usecase: Annotated[IEmployeeUC, Depends(get_employee_usecase)],
    ) -> Employee:
        """
        Update an employee person record.

        :param sid: UUID of the employee person.
        :param employee_in: Updated employee fields from request body.
        :param employee_usecase: Use case instance handling employee logic.
        :return: Updated employee data.
        """

        return await employee_usecase.update(
            sid=sid,
            employee_in=employee_in,
        )

    @staticmethod
    async def delete_employee(
        sid: UUID,
        employee_usecase: Annotated[IEmployeeUC, Depends(get_employee_usecase)],
    ) -> Msg:
        """
        Delete an employee person record.

        :param sid: UUID of the employee person.
        :param employee_usecase: Use case instance handling employee logic.
        :return: Confirmation message.
        """

        return await employee_usecase.delete(sid=sid)
