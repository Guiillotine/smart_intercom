from typing import Generic, TypeVar

from pydantic import field_validator

from src.common.constants import ErrorCodesEnums
from src.common.errors import BackendException
from src.common.schemas import CoreSchema

ItemSchema = TypeVar("ItemSchema")


class Pagination(CoreSchema):
    """
    Represents pagination parameters with validation for limit and offset values.

    This model ensures valid pagination parameters with non-negative values for both
    limit (number of items per page) and offset (number of records to skip).
    Provides default values for standard pagination behavior.

    :param limit: Maximum number of items to return per page (default: 100)
    :param offset: Number of items to skip before returning results (default: 0)
    """

    limit: int = 50
    offset: int = 0

    @field_validator("limit")
    @classmethod
    def validate_limit(cls, v: int | None) -> int | None:
        """
        Validate that the limit value is non-negative.

        Ensures the pagination limit parameter is either None or a non-negative integer.
        Preserves the input value when validation passes.

        :param cls: The pydantic model class containing this validator
        :param v: The value to validate (maximum number of items per page)
        :return: The validated value if validation succeeds
        """
        if v is not None and v < 0:
            raise BackendException(
                error=ErrorCodesEnums().Common.NUMBER_OUT_OF_BOUNDS,
                cause="Limit cannot be negative",
            )

        return v

    @field_validator("offset")
    @classmethod
    def validate_offset(cls, v: int | None) -> int | None:
        """
        Validate that the offset value is non-negative.

        Ensures the pagination offset parameter is either None or a non-negative integer.
        Preserves the input value when validation passes.

        :param cls: The pydantic model class containing this validator
        :param v: The value to validate (number of records to skip)
        :return: The validated value if validation succeeds
        """
        if v is not None and v < 0:
            raise BackendException(
                error=ErrorCodesEnums().Common.NUMBER_OUT_OF_BOUNDS,
                cause="Offset cannot be negative",
            )

        return v


class PaginationResult(CoreSchema, Generic[ItemSchema]):
    items: list[ItemSchema]
    limit: int
    offset: int
    total: int
