import random
from uuid import UUID

from fastapi import UploadFile

from src.common.schemas import Msg, Pagination, PaginationResult, SortBase
from src.modules.persons.interfaces import IEmployeeUC, IPersonSrv
from src.modules.persons.schemas import (
    Employee,
    EmployeeUpdate,
    PersonCreate,
    PersonUpdate, EmployeeCreate,
)
from src.modules.persons.usecases.constants import EmployeeUCEnums


class EmployeeUC(IEmployeeUC):
    """
    Use case class for employee operations over shared person records.

    This class maps employee API actions to the common person service and applies the
    employee person type where needed.
    """

    def __init__(
        self,
        enums: EmployeeUCEnums,
        employee_service: IPersonSrv,
    ):
        """
        Initializes EmployeeUC with the employee service dependency.

        :param employee_service: Service for managing employee records.
        """

        self._enums = enums
        self._employee_service = employee_service

    async def get_all(
        self, pagination_params: Pagination
    ) -> PaginationResult[Employee]:
        persons = await self._employee_service.get_all_paginated(
            pagination_params=pagination_params,
            sort_params=SortBase(
                sort_field=self._enums.PersonSchema.PersonSortField.full_name
            )
        )
        return PaginationResult(
            items=[Employee.model_validate(person) for person in persons.items],
            limit=persons.limit,
            offset=persons.offset,
            total=persons.total,
        )

    async def create(
        self,
        photo: UploadFile,
        employee_in: EmployeeCreate,
    ) -> Employee:
        # TODO: save photo
        photo_s3_path = ""

        # TODO: calculate embedding
        random.seed(42)
        face_embedding = [random.random() for _ in range(1536)]

        return Employee.model_validate(
            await self._employee_service.create(
                person_in=PersonCreate(
                    **employee_in.model_dump(),
                    photo=photo_s3_path,
                    face_embedding=face_embedding,
                )
            )
        )

    async def update(
        self,
        sid: UUID,
        employee_in: EmployeeUpdate,
        photo: UploadFile | None = None,
    ) -> Employee:
        employee = await self._employee_service.get_by_sid(sid)

        person_in = PersonUpdate.model_validate(employee_in)

        if photo is not None:
            # TODO: replace photo employee.photo -> photo
            photo_s3_path = ""

            # TODO: calculate embedding
            random.seed(42)
            face_embedding = [random.random() for _ in range(1536)]

            person_in.photo = photo_s3_path
            person_in.face_embedding = face_embedding

        return Employee.model_validate(
            await self._employee_service.update(
                sid=sid,
                person_in=person_in,
            )
        )

    async def delete(self, sid: UUID) -> Msg:
        return await self._employee_service.soft_delete(sid)
