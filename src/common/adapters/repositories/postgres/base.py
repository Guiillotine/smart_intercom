import logging
from contextlib import suppress
from typing import TypeVar, Any
from uuid import UUID

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import BaseModel
from sqlalchemy import Select, select, func, Column
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.associationproxy import AssociationProxyInstance
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm.base import SQLORMOperations
from sqlalchemy.sql.base import ExecutableOption

from src.common.constants import ErrorCodesEnums
from src.common.decorators import LoggingFunctionInfo
from src.common.errors import BackendException
from src.common.interfaces import IPostgresBaseRepo
from src.common.schemas import SQLFilterBase, SortBase, Pagination
from src.common.schemas.constants.enums import SortDirectionEnum

ModelType = TypeVar("ModelType", bound="CoreModel")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
FilterSchemaType = TypeVar("FilterSchemaType", bound=Filter)


class PostgresBaseRepo(
    IPostgresBaseRepo[ModelType, CreateSchemaType, UpdateSchemaType]
):

    def __init__(
        self,
        db: AsyncSession,
        model: type[ModelType],
        errors: ErrorCodesEnums,
        logger: logging.Logger,
    ):
        """
        Initialize the CRUD repository with model, database session, error handler, and
        logger.

        :param db: SQLAlchemy asynchronous session for database operations.
        :param model: SQLAlchemy ORM model class to operate on.
        :param errors: Error enumerations to raise domain-specific exceptions.
        :param logger: Logger instance used for logging internal actions.
        """

        self._db = db
        self._model = model
        self._errors = errors
        self._logger = logger

    @staticmethod
    async def _apply_options(
        query: Select,
        filters: SQLFilterBase = None,
        options: tuple[ExecutableOption, ...] | None = None,
    ) -> Select:
        if options:
            query = query.options(*options)
        if filters:
            query = filters.filter(query)
        return query

    async def _get_single_result(self, query: Select) -> ModelType | None:
        result = await self._db.execute(query)
        return result.scalars().first()

    async def _get_all_results(self, query: Select) -> list[ModelType]:
        result = await self._db.execute(query)
        return list(result.unique().scalars().all())

    async def _commit_and_refresh(self, db_obj: ModelType, with_commit: bool) -> None:
        if with_commit:
            await self._db.commit()
            await self._db.refresh(db_obj)
            self._logger.debug("%s created and committed", self._model.__name__)
        else:
            await self._db.flush()
            self._logger.debug("%s created and flushed", self._model.__name__)

    async def _apply_pagination(
        self,
        query: Select,
        pagination_params: Pagination,
    ) -> tuple[list[ModelType], int]:
        count_query = select(func.count()).select_from(query.subquery())
        total = await self._get_single_result(query=count_query)

        paginated_query = query.limit(pagination_params.limit).offset(
            pagination_params.offset
        )
        items = await self._get_all_results(query=paginated_query)

        return list(items), total

    async def _validate_sort_field(self, field_name: str) -> Column | SQLORMOperations:
        invalid_field_msg = "Invalid sort field: {field_name}"
        not_column_msg = "Not a column field: {field_name}"
        proxy_field_msg = "Cannot sort by proxy field: {field_name}"
        hybrid_msg = "Cannot sort by hybrid property: {field_name}"

        if not hasattr(self._model, field_name):
            raise ValueError(invalid_field_msg.format(field_name=field_name))

        field = getattr(self._model, field_name)
        field_descriptor = self._model.__dict__.get(field_name)

        if isinstance(field, AssociationProxyInstance):
            remote_attr = field.remote_attr
            if remote_attr is None:
                raise ValueError(proxy_field_msg.format(field_name=field_name))
            return remote_attr

        if isinstance(field_descriptor, hybrid_property):
            try:
                return field.expression
            except (AttributeError, NotImplementedError) as e:
                raise ValueError(hybrid_msg.format(field_name=field_name)) from e

        if field_name not in self._model.__table__.columns:
            raise ValueError(not_column_msg.format(field_name=field_name))

        return field

    async def _apply_sorts(
        self,
        query: Select,
        sort_params: SortBase,
    ) -> Select:
        if sort_params and sort_params.sort_field:
            try:
                sort_field = await self._validate_sort_field(sort_params.sort_field)

                if sort_params.direction == SortDirectionEnum.DESC:
                    sort_field = sort_field.desc()

                with suppress(AttributeError, NotImplementedError):
                    sort_field = sort_field.nulls_last()

            except ValueError as e:
                raise BackendException(
                    error=self._errors.Common.INCORRECT_SORT_FIELD
                ) from e

            else:
                return query.order_by(sort_field)

        return query

    @LoggingFunctionInfo(
        description="Fetch a single record by its SID from the database"
    )
    async def get_by_sid(
        self, sid: UUID, custom_options: tuple[ExecutableOption, ...] = None
    ) -> ModelType | None:
        query = await self._apply_options(
            query=select(self._model).where(self._model.sid == sid),
            options=custom_options,
        )

        self._logger.debug("Fetching %s by SID: %s", self._model.__name__, sid)
        return await self._get_single_result(query)

    @LoggingFunctionInfo(
        description="Retrieve all records of the model from the database"
    )
    async def get_all(
        self,
        filters: SQLFilterBase = None,
        sort_params: SortBase = None,
        custom_options: tuple[ExecutableOption, ...] = None,
    ) -> list[ModelType]:
        query = await self._apply_options(
            query=select(self._model), filters=filters, options=custom_options
        )

        self._logger.debug("Fetching all %s records", self._model.__name__)
        return list(await self._get_all_results(query))

    @LoggingFunctionInfo(
        description="Retrieve all records of the model with pagination"
    )
    async def get_all_paginated(
        self,
        pagination_params: Pagination,
        filters: SQLFilterBase = None,
        sort_params: SortBase = None,
        custom_options: tuple[ExecutableOption, ...] = None,
    ) -> tuple[list[ModelType], int]:
        query = await self._apply_options(
            query=select(self._model), filters=filters, options=custom_options
        )

        if filters:
            query = filters.filter(query)

        if sort_params:
            query = await self._apply_sorts(query, sort_params)

        return await self._apply_pagination(
            query=query,
            pagination_params=pagination_params,
        )

    @LoggingFunctionInfo(description="Create a new record in the database")
    async def create(
        self, *, obj_in: CreateSchemaType, with_commit: bool = True
    ) -> ModelType:
        try:
            db_obj = self._model(**obj_in.model_dump())
            self._db.add(db_obj)

            await self._commit_and_refresh(db_obj, with_commit)

        except IntegrityError as e:
            self._logger.debug(
                "Failed to create %s due to IntegrityError", self._model.__name__
            )
            raise BackendException(error=self._errors.Common.NOT_UNIQUE) from e

        else:
            return db_obj

    @LoggingFunctionInfo(description="Update an existing record in the database")
    async def update(
        self,
        *,
        db_obj: ModelType,
        obj_in: UpdateSchemaType | dict[str, Any],
        with_commit: bool = True,
    ) -> ModelType:
        try:
            update_data = (
                obj_in
                if isinstance(obj_in, dict)
                else obj_in.model_dump(exclude_unset=True)
            )

            for field, value in update_data.items():
                if hasattr(db_obj, field):
                    setattr(db_obj, field, value)

            self._db.add(db_obj)

            if with_commit:
                await self._db.commit()
                await self._db.refresh(db_obj)
                self._logger.debug(
                    "%s with SID=%s updated and committed",
                    self._model.__name__,
                    getattr(db_obj, "sid", "?"),
                )
            else:
                await self._db.flush()
                self._logger.debug(
                    "%s with SID=%s updated and flushed",
                    self._model.__name__,
                    getattr(db_obj, "sid", "?"),
                )

        except IntegrityError as e:
            self._logger.debug(
                "Failed to update %s due to IntegrityError", self._model.__name__
            )
            raise BackendException(error=self._errors.Common.NOT_UNIQUE) from e
        else:
            return db_obj

    @LoggingFunctionInfo(description="Delete a record from the database by its SID")
    async def delete(self, *, sid: UUID, with_commit: bool = True) -> ModelType | None:
        obj = await self.get_by_sid(sid)
        if obj is None:
            self._logger.debug(
                "%s with SID={sid} not found for deletion", self._model.__name__
            )
            return None

        await self._db.delete(obj)

        if with_commit:
            await self._db.commit()
            self._logger.debug(
                "%s with SID={sid} deleted and committed", self._model.__name__
            )
        else:
            await self._db.flush()
            self._logger.debug(
                "%s with SID={sid} deleted and flushed", self._model.__name__
            )

        return obj
