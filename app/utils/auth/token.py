from datetime import datetime, timedelta

from pydantic import BaseModel
from jose import jwt

import settings


SECRET_KEY = getattr(settings, 'SECRET_KEY')

ALGORITHM = getattr(settings, 'JWT_HASH_ALGORITHM')


class Token(BaseModel):
    access_token: str
    toke_type: str

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithm=[ALGORITHM])
    return payload

