import uvicorn

from commands.base import BaseCommand

class RunserverCommand(BaseCommand):
    _name = 'runserver'
    description = 'command to runserver'

    @classmethod
    def handler(cls, host: str, port: int, reload: bool) -> None:
        uvicorn.run("main:app", host=host, port=port, reload=reload)

    @classmethod
    def add_arguments(cls, parser) -> None:
        parser.add_argument(
                '-H',
                '--host',
                nargs='?',
                type=str,
                default='127.0.0.1',
            )
        parser.add_argument(
                '-P',
                '--port',
                nargs='?',
                type=int,
                default=8000,
            )
        parser.add_argument(
                '-R',
                '--reload',
                action='store_true',
            )