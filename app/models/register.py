from sqlmodel import SQLModel
from typing import Type


class PermissionRegistered:
    _instance = None
    _models = {}

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    def __call__(self, model: Type[SQLModel], methods=('create', 'read', 'update', 'delete')):
        if not issubclass(model, SQLModel):
            raise TypeError('Model should be subclass of SQLModel')
        if model.__tablename__ not in self._models:
            self._models[model.__tablename__] = methods

    @property
    def models(self):
        return [
            (f'{k}:{v}', f'{k}:{v}')
            for k, vs in self._models.items()
            for v in vs
        ]


def register(model, methods=('create', 'read', 'update', 'delete')):
    PermissionRegistered()(model, methods)
    return model

