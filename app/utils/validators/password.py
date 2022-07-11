from abc import abstractmethod
from difflib import SequenceMatcher

from .base import BaseValidator
from exceptions.exceptions import ValidationError


class BasePasswordValidator(BaseValidator):
    @abstractmethod
    def validate(self, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        if not self.validate(*args, **kwargs):
            raise ValidationError({'password': self})


class MinLengthValidator(BasePasswordValidator):
    message: str = 'Minimal password length must be equal or higher than {0}'

    def __init__(self, min_length: int = 8):
        self.min_length = min_length

    def __repr__(self):
        return self.message.format(self.min_length)

    def validate(self, password: str):
        return len(password) >= self.min_length


class SimilarPasswordUsernameValidator(BasePasswordValidator):
    message: str = 'Username and password too similar'
    username: str = None

    def __repr__(self):
        return self.message

    def validate(self, password: str):
        if not self.username:
            raise TypeError('Username must be set')
        if self.username in password \
                or password in self.username \
                or SequenceMatcher(None, password, self.username).ratio() > 0.5:
            return False
        return True


