from abc import ABC, abstractmethod
from uuid import UUID

from fastapi.security import OAuth2PasswordRequestForm

from src.modules.users.schemas import UserCreate, UserWithPassword, UserWithRole, User, \
    LoginToken, AccessToken, UserCreateInDB


class IUserSrv(ABC):
    """
    Interface for user service operations.

    Defines business operations for users.
    """

    @abstractmethod
    async def get_by_sid(self, sid: UUID) -> UserWithRole:
        """
        Get user by identifier.

        :param sid: User SID.
        :return: User data with role.
        """
        ...

    @abstractmethod
    async def get_by_email(self, email: str) -> UserWithPassword | None:
        """
        Get user by email.

        :param email: User email.
        :return: User data with password hash or None.
        """
        ...

    @abstractmethod
    async def create(self, user_in: UserCreateInDB) -> UserWithRole:
        """
        Create user.

        :param user_in: User creation schema.
        :return: Created user data with role.
        """
        ...


class IAuthSrv(ABC):
    """
    Interface for authentication management.

    This interface defines methods for authenticating users based on provided
    credentials and returning user data upon successful authentication. Implementations
    should handle authentication logic, such as verifying credentials and fetching
    user details.
    """

    @abstractmethod
    async def authenticate(self, credentials: OAuth2PasswordRequestForm) -> User:
        """
        Authenticate a user based on the provided credentials.

        :param credentials: The login credentials containing username (email) and
                password.
        :return: An instance of UserInDBBase with user information if authentication
                is successful.
        """
        ...


class ITokenProviderSrv(ABC):
    """
    Abstract interface for token service.

    This interface defines the contract for working with JWT tokens.
    Implementations must provide logic for generating access/refresh token pairs
    and validating existing tokens.
    """

    @abstractmethod
    async def create_token_pair(self, payload: dict) -> LoginToken:
        """
        Generates a pair of access and refresh tokens for a given payload.

        :param payload: Dictionary containing user information to encode in the token.
        :return: LoginToken object with access and refresh tokens.
        """
        ...

    @abstractmethod
    async def create_access_token(self, entity_sid: UUID, payload: dict) -> AccessToken:
        """
        Create access JWT token and register it in Redis.

        :param entity_sid: UUID of the token owner's entity.
        :param payload: Info to include in token (must contain 'sub').
        :return: AccessToken containing access tokens.
        """
        ...

    @abstractmethod
    async def validate_token(self, token: str) -> dict:
        """
        Validates the given token and returns its decoded payload.

        :param token: JWT token string to validate.
        :return: Dictionary representing the decoded token payload.
        """
        ...

    @abstractmethod
    async def delete_token(self, key: str):
        """
        Asynchronously delete a token identified by the given key.

        :param key: The key corresponding to the token that needs to be deleted.
        """
        ...

    @abstractmethod
    async def delete_user_tokens(self, prefix: str):
        """
        Asynchronously delete all tokens associated with a user, identified by the
        given key prefix.

        :param prefix: The prefix used to match and delete all related tokens
                (e.g., user identifier).
        """
        ...

    @abstractmethod
    async def get_token_by_key(self, key: str) -> str:
        """
        Asynchronously retrieve the token associated with the given key.

        :param key: The key for which the token needs to be fetched.
        :return: The token string retrieved from the storage.
        """
        ...

    @staticmethod
    @abstractmethod
    def prepare_token_key(entity_sid: UUID, pair_id: UUID, jti: UUID) -> str:
        """
        Prepare token key.

        :param entity_sid: UUID of the token entity.
        :param pair_id: UUID of the pair id.
        :param jti: UUID of the jti.
        :return: The token string associated with the key.
        """
        ...
