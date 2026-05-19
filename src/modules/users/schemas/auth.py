from pydantic import BaseModel, Field


class AccessToken(BaseModel):
    access_token: str


class RefreshToken(BaseModel):
    refresh_token: str


class TokenData(BaseModel):
    sid: str = Field(description="User's sid")
    jti: str = Field(description="JWT ID")
    role: list[str] = Field(description="User's role")


class LoginToken(RefreshToken, AccessToken):
    pass
