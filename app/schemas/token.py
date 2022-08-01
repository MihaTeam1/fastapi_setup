from pydantic import BaseModel, validator
from datetime import datetime

from models.token import TokenModel, TokenBase, Base


class RefreshToken(BaseModel):
    refresh_token: str
    expire_in: datetime | None = None

    @property
    def token(self):
        return self.refresh_token


class AccessToken(BaseModel):
    access_token: str
    expire_in: datetime | None = None

    @property
    def token(self):
        return self.access_token


class ResponseToken(RefreshToken, AccessToken):
    refresh_token: str | None = None
    expire_in: int
    token_type: str

    @validator('expire_in', pre=True)
    def cast_expire_in(cls, v):
        if isinstance(v, datetime):
            return v.timestamp()
        return v


class TokenRead(TokenBase, Base):
    pass


class TokenCreate(TokenBase, Base):
    pass


class TokenReadWithUser(TokenRead):
    from schemas.user import UserRead
    user: UserRead | None = None


