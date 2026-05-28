import random
from uuid import UUID

from fastapi import UploadFile

from src.common.constants import ErrorCodesEnums
from src.common.errors import BackendException
from src.common.schemas import Msg, Pagination, PaginationResult, SortBase
from src.modules.faces.interfaces import IFaceAnalyzerSrv
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
        errors: ErrorCodesEnums,
        employee_service: IPersonSrv,
        face_analyzer_service: IFaceAnalyzerSrv,
    ):
        """
        Initializes EmployeeUC with the employee service dependency.

        :param employee_service: Service for managing employee records.
        """

        self._enums = enums
        self._errors = errors
        self._employee_service = employee_service
        self._face_analyzer_service = face_analyzer_service

    async def get_all(
        self,
        pagination_params: Pagination,
        sort_params: SortBase | None = None,
    ) -> PaginationResult[Employee]:
        if not sort_params:
            sort_params = SortBase(sort_field="last_name")

        persons = await self._employee_service.get_all_paginated(
            pagination_params=pagination_params,
            sort_params=sort_params,
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
        photo_s3_path = self._employee_service.save_photo(photo)

        face_embedding = await self._get_single_face_embedding(photo)

        return Employee.model_validate(
            await self._employee_service.create(
                person_in=PersonCreate(
                    **employee_in.model_dump(),
                    photo_s3_path=photo_s3_path,
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
            self._employee_service.delete_photo(employee.photo)
            person_in.photo_s3_path = self._employee_service.save_photo(photo)
            person_in.face_embedding = await self._get_single_face_embedding(photo)

        return Employee.model_validate(
            await self._employee_service.update(
                sid=sid,
                person_in=person_in,
            )
        )

    async def delete(self, sid: UUID) -> Msg:
        return await self._employee_service.soft_delete(sid)

    async def _get_single_face_embedding(self, photo: UploadFile) -> list[float]:
        faces = await self._face_analyzer_service.analyse_photo(photo)
        if len(faces) != 1:
            raise BackendException(self._errors.Person.INCORRECT_PHOTO)

        return faces[0].face_embedding
