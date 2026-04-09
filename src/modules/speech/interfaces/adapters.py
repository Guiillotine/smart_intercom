from abc import ABC, abstractmethod

from src.common.interfaces import IS3BaseRepo


class ISpeechS3Repo(IS3BaseRepo, ABC):
    """
    Interface for speech-specific S3 repository.

    Defines additional speech-related S3 operations beyond the basic S3 repository
    functionality.
    """
    ...

    @abstractmethod
    async def put_audio_message(self, key: str, data: bytes) -> str:
        """
        Upload an audio message to the specified S3 bucket.

        :param key: The key (path/filename) to assign to the object.
        :param data: The object's data as bytes.
        :return: key
        """
        ...
