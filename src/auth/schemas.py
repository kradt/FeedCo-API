from pydantic import BaseModel


class TokenSet(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"


class TokenData(BaseModel):
    user_id: int
    token_type: str
    scopes: list[str] | None = None
    exp: int
    iat: int
