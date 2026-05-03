from typing import Annotated

from fastapi import Depends

from src.common.constants import CommonEnums
from src.common.constants.deps import get_common_enums
from src.modules.users.constants import UserEnums


def get_user_common_enums(
    common_enums: Annotated[CommonEnums, Depends(get_common_enums)],
) -> UserEnums:
    """Dependency provider for UserEnums instance.

    :return: Initialized user constants enum instance
    """
    return UserEnums(common_enums=common_enums)
