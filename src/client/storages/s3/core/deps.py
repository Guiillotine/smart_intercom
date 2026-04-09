from typing import Annotated

from fastapi import Depends

from src.client.storages.s3.core import S3Connect
from src.client.storages.s3.interfaces import IS3Connect
from src.config.settings import Settings
from src.config.settings.deps import get_settings


async def get_s3_client(
    settings: Annotated[Settings, Depends(get_settings)],
) -> IS3Connect:

    return S3Connect(settings=settings)
