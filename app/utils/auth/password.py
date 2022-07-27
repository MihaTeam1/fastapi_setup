from typing import List, Type, Optional
from passlib.context import CryptContext

from utils.validators.password import BasePasswordValidator
from exceptions.exceptions import ValidationError
from settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SEED = getattr(settings, 'secret_key')


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_default_validators() -> List[Type[BasePasswordValidator]]:
    return getattr(settings, 'PASSWORD_VALIDATORS', [])


def validate_password(
            password: str,
            validators: List[Type[BasePasswordValidator]] | None = None,
            **kwargs,
        ) -> None:
    if not validators:
        validators = get_default_validators()

    error = ValidationError([])
    for validator in validators:
        try:
            validator(password=password, **kwargs)
        except ValidationError as err:
            error = ValidationError({'password': [err, error]})

    if error.has_errors:
        raise error


def generate_password(base: str, seed: str = SEED, **kwargs) -> str:
    validators = get_default_validators()
    for validator in validators:
        base = validator.generate_password(base=base, seed=seed, **kwargs)
    return base