from abc import abstractmethod
from difflib import SequenceMatcher
import string

from .base import BaseValidator
from exceptions.exceptions import ValidationError


class BasePasswordValidator(BaseValidator):
    @abstractmethod
    def validate(self, *args, **kwargs):
        pass

    def generate_password(self, *args, **kwargs) -> str:
        return kwargs.get('base')

    @staticmethod
    def get_seed_charnum(seed: str, char: str | int = 0, iters: int = 5) -> int:
        if isinstance(char, str):
            char = ord(char)
        for _ in range(iters):
            new_char = ord(seed[char % len(seed)])
            char = new_char if new_char != char else ord(seed[(char + 1) % len(seed)])
        return char

    def __call__(self, password: str, **kwargs):
        if not self.validate(password, **kwargs):
            raise ValidationError({'password': self})


class MinLengthValidator(BasePasswordValidator):
    message: str = 'Minimal password length must be equal or higher than {0}'

    def __init__(self, min_length: int = 8):
        self.min_length = min_length

    def __repr__(self):
        return self.message.format(self.min_length)

    def validate(self, password: str, **kwargs):
        return len(password) >= self.min_length

    def generate_password(self, base: str, seed: str, **kwargs):
        if len(base) < self.min_length + 5:
            for i in range(self.min_length - len(base) + 5):
                base += chr(self.get_seed_charnum(seed, base[i % len(base)]))
        return base


class SimilarPasswordUsernameValidator(BasePasswordValidator):
    message: str = 'Username and password too similar'

    def __init__(self, ratio: float = 0.5):
        self.ratio = ratio

    def validate(self, password: str, username: str, **kwargs):
        if username in password \
                or password in username \
                or SequenceMatcher(None, password, username).ratio() > self.ratio:
            return False
        return True

    def generate_password(self, base: str, seed: str, username: str, **kwargs):
        base = list(base)
        for i in range(len(base)):
            if not self.validate(password=''.join(base), username=username):
                base.insert(i * (i % 2 == ord(seed[len(seed) // 2]) * -1), base.pop(len(base) // 2))
            else:
                break
        return ''.join(base)


class ComparePasswordsValidator(BasePasswordValidator):
    message: str = 'Passwords aren\'t equal'

    def validate(self, password: str, confirm_password: str, **kwargs):
        if password != confirm_password:
            return False
        return True


class ASCIIPasswordValidator(BasePasswordValidator):
    alphabet: str = string.ascii_letters \
                        + string.digits \
                        + string.punctuation
    message: str = f'Password has character, which not in {alphabet}'

    def validate(self, password: str, **kwargs):
        if set(password) - set(self.alphabet):
            return False
        return True

    def generate_password(self, base: str, seed: str, *args, **kwargs) -> str:
        last_num = self.get_seed_charnum(seed)
        password = ''
        for char in base:
            password += self.alphabet[(self.get_seed_charnum(seed, ord(char)) + last_num) % len(self.alphabet)]
            last_num = ord(char)
        return password
