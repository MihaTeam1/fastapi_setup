from pathlib import Path
from jose.exceptions import ExpiredSignatureError
from pydantic import BaseSettings, PostgresDsn
from typing import Set, List, Dict, Callable, Type
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware

from utils import validators
from exceptions import ValidationError
from exceptions import handlers as exc_handlers


class Settings(BaseSettings):
    base_dir: Path = Path(__file__).parent.parent
    secret_key: str
    jwt_hash_algorythm: str = 'HS256'
    access_token_expire_minutes: int = 60
    refresh_token_expire_minutes: int = 60*24*30
    password_validators: List[validators.password.BasePasswordValidator] = [
            # validators.password.SimilarPasswordUsernameValidator(0.5),
            validators.password.ComparePasswordsValidator(),
            validators.password.MinLengthValidator(10),
            validators.password.ASCIIPasswordValidator(),
    ]
    exception_handlers: Dict[Type[Exception], Callable] = {
        ValidationError: exc_handlers.validation_error_handler,
        ExpiredSignatureError: exc_handlers.expired_signature_error_handler,
    }

    origins: Set[str]
    middleware: List[Middleware] = []

    pg_dsn: PostgresDsn
    pg_echo: bool = True
    pg_future: bool = True

    def __init__(self, module: Type[BaseSettings] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.middleware: List[Middleware] = [
                Middleware(
                    CORSMiddleware,
                    allow_origins=self.origins,
                    allow_credentials=True,
                    allow_methods=['*'],
                    allow_headers=['*']
                ),
            ]
        if module:
            self.__dict__.update(**module().__dict__)