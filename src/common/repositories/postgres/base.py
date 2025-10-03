#ModelType
from typing import TypeVar

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType", bound="CoreModel")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
FilterSchemaType = TypeVar("FilterSchemaType", bound=Filter)


class PostgresBaseRepo[ModelType, CreateSchemaType, UpdateSchemaType, FilterSchemaType]:
    def __init__(self, model: ModelType, db: AsyncSession):
        self._db = db
        self._model = model

    async def get_all(self):
        pass

    async def get_all_paginated(self):
        pass

    async def get_one(self):
        pass

    async def create(self):
        pass

    async def update(self):
        pass

    async def delete(self):
        pass

    async def add_and_refresh(self):
        pass
