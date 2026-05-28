from abc import ABC, abstractmethod
from uuid import UUID

from fastapi import UploadFile

from src.common.schemas import Msg, Pagination, PaginationResult, SortBase
from src.modules.persons.schemas import EmployeeCreate, Employee, EmployeeUpdate, \
    EmployeeCreate


class IEmployeeUC(ABC):
    """
    Interface for employee use case operations over shared person records.
    """

    @abstractmethod
    async def get_all(
        self,
        pagination_params: Pagination,
        sort_params: SortBase | None = None,
    ) -> PaginationResult[Employee]:
        """
        Retrieve a paginated list of employee person records.

        :param pagination_params: Pagination settings.
        :param sort_params: Optional sort params.
        :return: Paginated list of employees.
        """
        ...

    @abstractmethod
    async def create(
        self,
        photo: UploadFile,
        employee_in: EmployeeCreate,
    ) -> Employee:
        """
        Create an employee person record.

        :param photo: Employee photo.
        :param employee_in: Employee data for creation.
        :return: Created employee data.
        """
        ...

    @abstractmethod
    async def update(
        self,
        sid: UUID,
        employee_in: EmployeeUpdate,
        photo: UploadFile | None = None,
    ) -> Employee:
        """
        Update an employee person record.

        :param sid: UUID of the target employee person.
        :param employee_in: Updated employee fields.
        :param photo: Updated employee photo.
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
