from abc import ABC, abstractmethod
from uuid import UUID

from fastapi import APIRouter

from src.common.schemas import Msg, Pagination, PaginationResult
from src.modules.persons.interfaces.usecases import IEmployeeUC
from src.modules.persons.schemas import EmployeeCreate, Employee, EmployeeUpdate


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
        employee_in: EmployeeCreate,
        employee_usecase: IEmployeeUC,
    ) -> Employee:
        """
        Create an employee person record.

        :param employee_in: Employee data from request body.
        :param employee_usecase: Use case instance handling employee logic.
        :return: Created employee data.
        """
        ...

    @staticmethod
    @abstractmethod
    async def update_employee(
        sid: UUID,
        employee_in: EmployeeUpdate,
        employee_usecase: IEmployeeUC,
    ) -> Employee:
        """
        Update an employee person record.

        :param sid: UUID of the target employee person.
        :param employee_in: Updated employee fields from request body.
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
