from contextlib import AbstractAsyncContextManager

import aioboto3
from aiobotocore.client import AioBaseClient
from botocore.client import Config

from src.client.storages.s3.interfaces import IS3Connect
from src.config.settings import Settings


class S3Connect(IS3Connect):
    """
    Handles the creation and management of an aioboto3 S3 client using application
    settings for configuration. Provides access to the configured S3 client for
    performing storage operations.
    """

    def __init__(self, settings: Settings):
        """
        Initialize the S3Connect instance with the provided settings.

        :param settings: Application settings containing S3 configuration parameters.
        """

        self._settings = settings

    def _get_client(self) -> AioBaseClient:
        return aioboto3.Session().client(
            service_name="s3",
            endpoint_url=self._settings.s3.ENDPOINT_URL,
            aws_access_key_id=self._settings.s3.ACCESS_KEY,
            aws_secret_access_key=self._settings.s3.SECRET_KEY,
            region_name=self._settings.s3.REGION_NAME,
            config=Config(
                request_checksum_calculation="when_required",
                response_checksum_validation="when_required",
            ),
        )

    async def get_connect(self) -> AbstractAsyncContextManager:
        """
        Retrieve an asynchronous context manager for the configured aioboto3 S3 client.

        :return: Asynchronous context manager for the S3 client.
        """

        return self._get_client()
