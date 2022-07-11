import os
from pathlib import Path

from utils import validators
import exceptions

BASE_DIR = Path(__file__).parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY')
JWT_HASH_ALGORITHM = os.environ.get('JWT_HASH_ALGORITHM', 'HS256')
ACCESS_TOKEN_EXPIRE_MINUTES = 30


PASSWORD_VALIDATORS = [
    validators.password.MinLengthValidator(10),
    validators.password.SimilarPasswordUsernameValidator(),
]

exception_handlers = {
    exceptions.ValidationError: exceptions.handlers.validation_error_handler
}

settings = {
    'exception_handlers': exception_handlers
}