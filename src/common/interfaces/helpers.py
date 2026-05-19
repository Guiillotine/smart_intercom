from abc import abstractmethod, ABC
from datetime import timedelta, datetime
from uuid import UUID


class ITokenHelper(ABC):
    """
    Interface for Token Helper, responsible for token generation and validation.
    """

    @abstractmethod
    def create_token(
        self,
        jti: UUID,
        data: dict,
        pair_id: UUID,
        expires_delta: timedelta | None,
        refresh: bool = False,
    ) -> str:
        """
        Generates a JWT token based on provided data.

        :param jti: The unique identifier for the token.
        :param data: The data to be encoded in the token.
        :param pair_id: Unique sid of pair
        :param expires_delta: The expiration time for the token.
        :param refresh: Flag indicating whether the token is a refresh token.
        :return: The generated JWT token as a string.
        """
        ...

    @abstractmethod
    def decode_token(self, token: str) -> dict:
        """
        Decode the provided token and return its payload as a dictionary.

        :param token: Token string to decode.
        :return: Dictionary containing the decoded token payload.
        """
        ...


class ICustomDateTime(ABC):
    """
    Interface for datetime utilities.

    Provides methods to obtain the current datetime in either naive
    (timezone-unaware) or timezone-aware form, depending on application requirements.
    """

    @staticmethod
    @abstractmethod
    def get_utc_datetime() -> datetime:
        """
        Get the current UTC datetime without microseconds.

        :return: Naive datetime object (without timezone).
        """
        ...

    @staticmethod
    @abstractmethod
    def get_datetime_w_timezone() -> datetime:
        """
        Get the current datetime with timezone awareness based on application settings.

        :return: Aware datetime object localized to the configured timezone.
        """
        ...
