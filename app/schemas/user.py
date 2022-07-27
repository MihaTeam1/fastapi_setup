from typing import List, Optional
from pydantic import BaseModel, root_validator

from models.user import UserBase, User, UserBaseWithPassword, Base
from exceptions import ValidationError
from settings import settings
import logging

logger = logging.getLogger(__name__)


PASSWORD_VALIDATORS = getattr(settings, 'password_validators')


class UserCreate(UserBaseWithPassword):
    confirm_password: str

    @root_validator
    def validate_password(cls, values):
        error = ValidationError([])
        for validator in PASSWORD_VALIDATORS:
            try:
                params = {
                    k: values.get(k)
                    for k in validator.requires
                    if k in values
                }
                validator(
                    **params
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
    current_password: str
    new_password: str
    new_confirm_password: str

    @root_validator
    def validate_password(cls, values):
        error = ValidationError([])
        for validator in PASSWORD_VALIDATORS:
            try:
                params = {}
                for k in validator.requires:
                    if 'current' not in k:
                        if f'new_{k}' in values:
                            params[k] = values[f'new_{k}']
                    elif k in values:
                        params[k] = values[k]

                validator(
                    **params
                )
            except ValidationError as err:
                error = ValidationError({'password': [err, error]})
        if error.has_errors:
            raise error
        return values


class UserReadWithTokens(UserBase, Base):
    from .token import TokenRead
    tokens: List[TokenRead] = []