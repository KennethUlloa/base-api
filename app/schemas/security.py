from datetime import datetime
from pydantic import BaseModel, Field


class TokenDTO(BaseModel):
    access_token: str
    token_type: str


class AccessToken(BaseModel):
    sub: str
    exp: datetime | None = Field(default=None)
