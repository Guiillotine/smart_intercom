from abc import ABC, abstractmethod
from uuid import UUID

from src.common.schemas import Msg, Pagination, PaginationResult
from src.modules.persons.schemas import EmployeeCreate, Employee, EmployeeUpdate


class IEmployeeUC(ABC):
    """
    Interface for employee use case operations over shared person records.
    """

    @abstractmethod
    async def get_all(
        self,
        pagination_params: Pagination,
    ) -> PaginationResult[Employee]:
        """
        Retrieve a paginated list of employee person records.

        :param pagination_params: Pagination settings.
        :return: Paginated list of employees.
        """
        ...

    @abstractmethod
    async def create(
        self,
        employee_in: EmployeeCreate,
    ) -> Employee:
        """
        Create an employee person record.

        :param employee_in: Employee data for creation.
        :return: Created employee data.
        """
        ...

    @abstractmethod
    async def update(
        self,
        sid: UUID,
        employee_in: EmployeeUpdate,
    ) -> Employee:
        """
        Update an employee person record.

        :param sid: UUID of the target employee person.
        :param employee_in: Updated employee fields.
        :return: Updated employee data.
        """
        ...

    @abstractmethod
    async def delete(
        self,
        sid: UUID,
    ) -> Msg:
        """
        Delete an employee person record.

        :param sid: UUID of the target employee person.
        :return: Confirmation message.
        """
        ...
