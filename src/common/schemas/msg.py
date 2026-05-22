from pydantic import BaseModel


class Msg(BaseModel):
    content: str = "OK"
        