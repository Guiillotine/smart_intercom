import logging
from collections.abc import Sequence

from src.client.interfaces import IS3SessionProvider
from src.common.interfaces import IS3BaseRepo


class S3BaseRepo(IS3BaseRepo):
    """
    Interface for a class that initializes S3 storage infrastructure.

    Defines the contract for classes responsible for setting up S3 buckets and
    configuring notification settings or other initialization routines required
    for proper S3 usage in the application.
    """

    def __init__(self, s3_session_provider: IS3SessionProvider, logger: logging.Logger):
        """
        Initialize the S3BaseRepo instance.

        :param s3_session_provider: Provider for async S3 client sessions.
        :param logger: Logger instance for operation logging.
        """

        self._s3_session_provider = s3_session_provider
        self._logger = logger

    async def get_object(self, bucket: str, key: str) -> bytes:
        """
        Retrieve an object from S3 storage.

        :param bucket: Name of the S3 bucket.
        :param key: Key of the object to retrieve.
        :return: The object data as bytes.
        """

        async with self._s3_session_provider.get_session() as s3_client:
            response = await s3_client.get_object(Bucket=bucket, Key=key)
            data = await response["Body"].read()
            self._logger.debug("Downloaded object '%s' from bucket '%s'", key, bucket)
            return data

    async def put_object(self, bucket: str, key: str, data: bytes) -> str:
        """
        Upload an object to S3 storage.

        :param bucket: Name of the S3 bucket.
        :param key: Key of the object to upload.
        :param data: Data to upload as bytes.
        :return: None
        """

        key = key.replace(" ", "_")

        async with self._s3_session_provider.get_session() as s3_client:
            await s3_client.put_object(
                ACL="public-read",
                Bucket=bucket,
                Key=key,
                Body=data,
            )
            self._logger.debug("Uploaded object '%s' to bucket '%s'", key, bucket)

        return key

    async def delete_object(self, bucket: str, key: str) -> None:
        """
        Delete an object from S3 storage.

        :param bucket: Name of the S3 bucket.
        :param key: Key of the object to delete.
        :return: None
        """

        async with self._s3_session_provider.get_session() as s3_client:
            await s3_client.delete_object(Bucket=bucket, Key=key)
            self._logger.debug("Deleted object '%s' from bucket '%s'", key, bucket)

    async def list_objects(
        self, bucket: str, prefix: str | None = None
    ) -> Sequence[str]:
        """
        List objects in S3 storage, optionally filtered by prefix.

        :param bucket: Name of the S3 bucket.
        :param prefix: Optional prefix to filter object keys.
        :return: Sequence of object keys.
        """

        async with self._s3_session_provider.get_session() as s3_client:
            paginator = s3_client.get_paginator("list_objects_v2")
            keys = []
            async for page in paginator.paginate(Bucket=bucket, Prefix=prefix or ""):
                keys.extend(obj["Key"] for obj in page.get("Contents", []))
            self._logger.debug("Listed %d objects in bucket '%s'", len(keys), bucket)
            return keys
