import re
from uuid import UUID

from pydantic import EmailStr, Field, field_validator

from src.common.constants import ErrorCodesEnums
from src.common.errors import BackendException
from src.common.schemas import CoreSchema
from src.modules.users.schemas import RoleBase


class UserBase(CoreSchema):
    first_name: str
    last_name: str
    middle_name: str | None = None
    email: EmailStr

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        if " " in v:
            raise BackendException(
                error=ErrorCodesEnums().Common.UNPROCESSABLE_ENTITY,
                cause="Email must not contain spaces",
            )
        if len(v) > 254:  # noqa: PLR2004
            raise BackendException(
                error=ErrorCodesEnums().Common.UNPROCESSABLE_ENTITY,
                cause="Email length must be at most 254 characters",
            )
        return v

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not (2 <= len(v) <= 50):  # noqa: PLR2004
            raise BackendException(
                error=ErrorCodesEnums().Common.UNPROCESSABLE_ENTITY,
                cause="Name length must be between 2 and 50 characters",
            )
        if not re.fullmatch(r"[^\W\d_]+(?:-[^\W\d_]+)*", v, re.UNICODE):
            raise BackendException(
                error=ErrorCodesEnums().Common.UNPROCESSABLE_ENTITY,
                cause="Name must not contain digits or special symbols except hyphen",
            )
        return v


class UserWithSid(UserBase):
    sid: UUID


class UserCreate(UserBase):
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:  # noqa: PLR2004
            raise BackendException(
                error=ErrorCodesEnums().Common.UNPROCESSABLE_ENTITY,
                cause="Password must be at least 8 characters",
            )
        if not re.search(r"[A-Z]", v):
            raise BackendException(
                error=ErrorCodesEnums().Common.UNPROCESSABLE_ENTITY,
                cause="Password must contain at least one uppercase Latin letter",
            )
        if not re.search(r"[a-zA-Z]", v):
            raise BackendException(
                error=ErrorCodesEnums().Common.UNPROCESSABLE_ENTITY,
                cause="Password must contain Latin letters",
            )
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>_\-+=\\\/]", v):
            raise BackendException(
                error=ErrorCodesEnums().Common.UNPROCESSABLE_ENTITY,
                cause="Password must contain at least one special symbol",
            )
        return v


class User(UserBase):
    sid: UUID
    is_active: bool


class CreatedUser(User):
    hashed_password: str


class UserWithRole(User):
    role: RoleBase


class UserWithPassword(User):
    password_hash: str | None = None
