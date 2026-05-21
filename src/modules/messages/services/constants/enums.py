from src.common.constants import CommonEnums
from src.common.schemas.constants import SchemaEnums


class MessageSrvEnums:
    def __init__(
        self,
        common_enums: CommonEnums,
        schema_enums: SchemaEnums,
    ):
        self.Common = common_enums
        self.Schema = schema_enums
