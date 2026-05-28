from abc import ABC, abstractmethod
from uuid import UUID

from fastapi import APIRouter, UploadFile
from starlette.requests import Request

from src.common.schemas import Msg, Pagination, PaginationResult
from src.modules.persons.interfaces.usecases import IEmployeeUC
from src.modules.persons.schemas import Employee, EmployeeUpdate, \
    EmployeeCreate


class IEmployeeCtrl(ABC):
    """
    Interface for employee controller operations.
    """

    @property
    @abstractmethod
    def controller(self) -> APIRouter:
        """
        Get the configured APIRouter instance.

        :return: Configured FastAPI router with all employee routes.
        """
        ...

    @staticmethod
    @abstractmethod
    async def get_all_employees(
        pagination_params: Pagination,
        employee_usecase: IEmployeeUC,
    ) -> PaginationResult[Employee]:
        """
        Retrieve a paginated list of employee person records.

        :param pagination_params: Pagination settings.
        :param employee_usecase: Use case instance handling employee logic.
        :return: Paginated list of employees.
        """
        ...

    @staticmethod
    @abstractmethod
    async def create_employee(
        photo: UploadFile,
        first_name: str,
        last_name: str,
        employee_usecase: IEmployeeUC,
        middle_name: str | None = None,
    ) -> Employee:
        """
        Create an employee person record.

        :param photo: Employee photo.
        :param first_name: Employee first name.
        :param last_name: Employee last name.
        :param middle_name: Employee middle name.
        :param employee_usecase: Use case instance handling employee logic.
        :return: Created employee data.
        """
        ...

    @staticmethod
    @abstractmethod
    async def update_employee(
        sid: UUID,
        request: Request,
        employee_usecase: IEmployeeUC,
        photo: UploadFile | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
        middle_name: str | None = None,
    ) -> Employee:
        """
        Update an employee person record.

        :param sid: UUID of the target employee person.
        :param request: FastAPI request, used to distinguish omitted form fields.
        :param first_name: Updated employee first name.
        :param last_name: Updated employee last name.
        :param middle_name: Updated employee middle name.
        :param photo: Updated employee photo.
        :param employee_usecase: Use case instance handling employee logic.
        :return: Updated employee data.
        """
        ...

    @staticmethod
    @abstractmethod
    async def delete_employee(
        sid: UUID,
        employee_usecase: IEmployeeUC,
    ) -> Msg:
        """
        Delete an employee person record.

        :param sid: UUID of the target employee person.
        :param employee_usecase: Use case instance handling employee logic.
        :return: Confirmation message.
        """
        ...
