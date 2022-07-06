import argparse

class AutoRegister(type):
    def __new__(mcs, name, bases, classdict):
        new_cls = type.__new__(mcs, name, bases, classdict)
        for b in bases:
            if hasattr(b, 'register_subclass'):
                b.register_subclass(new_cls)
        return new_cls


class BaseCommand(metaclass=AutoRegister):
    _subclasses = []

    description = 'Process some integers.'
    _name = None

    @classmethod
    @property
    def name(cls):
        if cls._name:
            return cls._name
        else:
            return cls.__name__.lower()

    @classmethod
    def register_subclass(klass, cls):
        klass._subclasses.append(cls)

    @classmethod
    def get_concrete_classes(klass):
        return klass._subclasses

    @classmethod
    def get_parser(cls, *args, **kwargs) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(description=cls.description)
        cls.add_arguments(parser)
        return parser

    @classmethod
    def handler(cls, **options) -> None:
        raise NotImplementedError('handler must be implemented')

    @classmethod
    def start(cls, argv: list = None) -> None:
        parser = cls.get_parser()
        options = parser.parse_args(argv)
        cls.handler(**vars(options))

    @classmethod
    def add_arguments(cls, parser: argparse.ArgumentParser) -> None:
        pass








