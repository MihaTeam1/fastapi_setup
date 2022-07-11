from typing import List, Type, Optional
from passlib.context import CryptContext

from utils.validators.password import *
from exceptions.exceptions import ValidationError
import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_default_validators() -> List[Type[BasePasswordValidator]]:
    return getattr(settings, 'PASSWORD_VALIDATORS', [])


def validate_password(
            password: str,
            validators: List[Type[BasePasswordValidator]] | None = None,
            username: Optional[str] = None,
        ) -> None:
    if not validators:
        validators = get_default_validators()

    error = ValidationError([])
    for validator in validators:
        try:
            if username and hasattr(validator, 'username'):
                validator.username = username
            validator(password=password)
        except ValidationError as err:
            error = ValidationError({'password':[err, error]})

    if error.has_errors:
        raise error


def compare_passwords(password1: str, password2: str) -> None:
    if password1 != password2:
        raise ValidationError({'password': 'Passwords are not equal'})
