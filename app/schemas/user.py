from typing import List, Optional
from pydantic import BaseModel, root_validator

from models.user import UserBase, User, UserBaseWithPassword, Base
from exceptions import ValidationError
from settings import settings


PASSWORD_VALIDATORS = getattr(settings, 'password_validators')


class UserCreate(UserBaseWithPassword):
    confirm_password: str

    @root_validator
    def validate_password(cls, values):
        error = ValidationError([])
        for validator in PASSWORD_VALIDATORS:
            try:
                validator(
                    password=values.get('password'),
                    confirm_password=values.get('confirm_password'),
                    username=values.get('username')
                )
            except ValidationError as err:
                error = ValidationError({'password': [err, error]})
        if error.has_errors:
            raise error
        return values


class UserRead(UserBase, Base):
    pass


class UserLogin(UserBaseWithPassword):
    pass


class UserChangePassword(BaseModel):
    password: str
    new_password: str
    new_confirm_password: str


class UserReadWithTokens(UserBase, Base):
    from .token import TokenRead
    tokens: List[TokenRead] = []