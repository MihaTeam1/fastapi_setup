from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from models.token import Token, TokenBase, Base


class RefreshToken(BaseModel):
    refresh_token: str
    expire_in: Optional[datetime] = None

    @property
    def token(self):
        return self.refresh_token


class AccessToken(BaseModel):
    access_token: str
    expire_in: Optional[datetime] = None

    @property
    def token(self):
        return self.access_token


class ResponseToken(RefreshToken, AccessToken):
    expire_in: datetime
    token_type: str


class TokenRead(TokenBase, Base):
    pass


class TokenCreate(TokenBase, Base):
    pass


class TokenReadWithUser(TokenRead, Base):
    from schemas.user import UserRead
    user: Optional[UserRead] = None


