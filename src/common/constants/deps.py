from src.common.constants import CommonEnums, ErrorCodesEnums


def get_common_enums():
    """Dependency provider for common enums."""
    return CommonEnums()


def get_error_codes_enums():
    """Dependency provider for error code enums."""
    return ErrorCodesEnums()
