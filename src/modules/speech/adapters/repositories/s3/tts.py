import logging

from src.client.interfaces import IS3SessionProvider
from src.common.adapters.repositories.s3 import S3BaseRepo
from src.config.settings import Settings
from src.modules.speech.interfaces import ISpeechS3Repo


class SpeechS3Repo(S3BaseRepo, ISpeechS3Repo):
    """
    A repository for managing audio recordings of speech in the C3 storage.
    Inherits from S3BaseRepo for core S3 operations and implements ISpeechS3Repo.
    """

    def __init__(
        self,
        logger: logging.Logger,
        s3_session_provider: IS3SessionProvider,
        settings: Settings,
    ):
        super().__init__(s3_session_provider=s3_session_provider, logger=logger)
        self._logger = logger
        self._settings = settings

    async def put_audio_message(self, key: str, data: bytes) -> str:
        return await self.put_object(
            bucket=self._settings.s3.MESSAGE_BUCKET_NAME,
            key=key,
            data=data,
        )
