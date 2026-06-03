import logging
from typing import TYPE_CHECKING
from uuid import UUID

from fastapi import UploadFile

from src.common.constants import ErrorCodesEnums
from src.common.decorators import LoggingFunctionInfo
from src.common.errors import BackendException
from src.common.schemas import Msg, Pagination, PaginationResult, SortBase
from src.config.settings import Settings
from src.modules.persons.filters import PersonFilter
from src.modules.persons.interfaces import IPersonPostgresRepo, IPersonSrv, \
    IPersonS3Repo
from src.modules.persons.schemas import PersonCreate, Person, PersonUpdate, \
    PersonPhotoResponse
from src.modules.persons.services.constants import PersonSrvEnums

if TYPE_CHECKING:
    from src.modules.persons.models import PersonModel


class PersonSrv(IPersonSrv):
    """
    Service layer for managing shared person records.

    Provides business logic operations related to persons and delegates database
    interactions to the person repository.
    """

    def __init__(
        self,
        enums: PersonSrvEnums,
        errors: ErrorCodesEnums,
        logger: logging.Logger,
        settings: Settings,
        person_s3_repo: IPersonS3Repo,
        person_postgres_repo: IPersonPostgresRepo,
    ):
        """
        Initialize the person service with dependencies.
        """

        self._enums = enums
        self._errors = errors
        self._logger = logger
        self._settings = settings
        self._person_photo_bucket_name = settings.s3.PERSON_PHOTO_BUCKET_NAME
        self._person_s3_repo = person_s3_repo
        self._person_postgres_repo = person_postgres_repo

    @LoggingFunctionInfo(description="Get person by sid.")
    async def get_by_sid(self, sid: UUID) -> Person:
        return Person.model_validate(
            await self._person_postgres_repo.get_by_sid(sid)
        )

    @LoggingFunctionInfo(description="Search person by face embedding.")
    async def search_by_face_embedding(self, embedding: list[float]) -> UUID | None:
        return await self._person_postgres_repo.search_by_face_embedding(
            embedding=embedding,
            max_distance=self._settings.face.FACE_RECOGNITION_MAX_DISTANCE,
        )

    @LoggingFunctionInfo(description="Create person.")
    async def create(self, person_in: PersonCreate) -> Person:
        return Person.model_validate(
            await self._person_postgres_repo.create(obj_in=person_in)
        )

    @LoggingFunctionInfo(description="Upload person photo.")
    async def save_person_photo(
        self,
        photo: UploadFile,
        embedding: list[float],
    ) -> PersonPhotoResponse:
        key = f"{self._enums.Common.S3Prefix.PERSON}/{photo.filename}"
        self._logger.debug("Uploading photo with key: %s", key)

        key = await self._person_s3_repo.put_object(
            bucket=self._person_photo_bucket_name,
            key=key,
            data=await photo.read(),
        )

        return PersonPhotoResponse(path=f"{self._person_photo_bucket_name}/" + key)

    @LoggingFunctionInfo(description="Upload person photo.")
    async def update_person_photo(
        self,
        sid: UUID,
        photo: UploadFile,
        embedding: list[float],
    ) -> PersonPhotoResponse:
        person = await self._get_model_by_sid(sid)

        if person.photo_s3_path is not None:
            await self._delete_person_photo(key=person.photo_s3_path)

        key = f"{self._enums.Common.S3Prefix.PERSON}/{photo.filename}"
        self._logger.debug("Uploading photo with key: %s", key)

        key = await self._person_s3_repo.put_object(
            bucket=self._person_photo_bucket_name,
            key=key,
            data=await photo.read(),
        )

        path = await self._update_person_photo(
            key=key,
            person=person,
            embedding=embedding,
        )

        return PersonPhotoResponse(path=path)


    @LoggingFunctionInfo(description="Update person.")
    async def update(self, sid: UUID, person_in: PersonUpdate) -> Person:
        person = await self._get_model_by_sid(sid)

        return Person.model_validate(
            await self._person_postgres_repo.update(
                db_obj=person,
                obj_in=person_in,
            )
        )

    @LoggingFunctionInfo(description="Get person list.")
    async def get_all_paginated(
        self,
        pagination_params: Pagination,
        filters: PersonFilter = None,
        sort_params: SortBase = None,
    ) -> PaginationResult[Person]:
        persons, total = await self._person_postgres_repo.get_all_paginated(
            pagination_params=pagination_params,
            sort_params=sort_params,
            filters=filters,
        )

        return PaginationResult(
            items=[Person.model_validate(person) for person in persons],
            limit=pagination_params.limit,
            offset=pagination_params.offset,
            total=total,
        )

    @LoggingFunctionInfo(description="Delete person.")
    async def soft_delete(self, sid: UUID) -> Msg:
        person = await self._get_model_by_sid(sid)

        if not person:
            raise BackendException(error=self._errors.Person.PERSON_NOT_FOUND)

        await self._person_postgres_repo.update(
            db_obj=person,
            obj_in=PersonUpdate(is_archived=True),
        )

        return Msg()

    async def _get_model_by_sid(
        self,
        sid: UUID,
    ) -> "PersonModel":
        person = await self._person_postgres_repo.get_by_sid(sid)

        if not person:
            raise BackendException(self._errors.Person.PERSON_NOT_FOUND)

        return person

    @LoggingFunctionInfo(description="Update person photo path in the database.")
    async def _update_person_photo(
        self,
        key: str,
        person: "PersonModel",
        embedding: list[float],
    ) -> str:
        self._logger.debug("Updating avatar for person: %s", person.sid)
        photo_s3_path = f"{self._person_photo_bucket_name}/" + key

        await self._person_s3_repo.update(
            db_obj=person,
            obj_in=PersonUpdate(
                face_embedding=embedding,
                photo_s3_path=photo_s3_path,
            ),
        )

        return photo_s3_path

    @LoggingFunctionInfo(description="Delete person photo from S3 storage.")
    async def _delete_person_photo(self, key: str) -> None:
        key = key.replace(f"{self._person_photo_bucket_name}/", "/")

        self._logger.debug("Deleting photo with key: %s", key)
        await self._person_s3_repo.delete_object(
            bucket=self._person_photo_bucket_name, key=key
        )
