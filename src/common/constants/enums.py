from enum import StrEnum


class RequestTypesEnum(StrEnum):
    GET = "get"
    POST = "post"
    PUT = "put"
    DELETE = "delete"


class CommonEnums:
    def __init__(self):
        self.RequestTypes = RequestTypesEnum
