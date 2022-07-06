from .runserverCommand import RunserverCommand
from .shellCommand import ShellCommand

from .base import BaseCommand

def process(argv):
    command = None
    if len(argv) > 1:
        for i in BaseCommand.get_concrete_classes():
            if i.name == argv[1]:
                command = i
                argv.pop(0)
                break
    if command is None:
        print("Type 'manage.py help <subcommands>' for help in specific subcommand\n")
        for command in BaseCommand.get_concrete_classes():
            print(f'{command.name}')
        return
    command.start()
