from src.common.constants import CommonEnums, ErrorCodesEnums, TokenEnums


def get_common_enums():
    """Dependency provider for common enums."""
    return CommonEnums()


def get_token_enums():
    """Dependency provider for token enums."""
    return TokenEnums()


def get_error_codes_enums():
    """Dependency provider for error code enums."""
    return ErrorCodesEnums()
