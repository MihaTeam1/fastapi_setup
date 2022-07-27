from abc import ABC, abstractmethod

from exceptions.exceptions import ValidationError


class BaseValidator(ABC):
    message: str

    def __call__(self, *args, **kwargs):
        if not self.validate(*args, **kwargs):
            raise ValidationError(self)

    def __repr__(self, *args, **kwargs):
        return self.message

    @abstractmethod
    def validate(self, *args, **kwargs):
        pass


