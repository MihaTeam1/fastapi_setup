import code

from commands.base import BaseCommand

class ShellCommand(BaseCommand):
    _name = 'shell'
    description = 'run python interactive terminal in fastapi env'

    @classmethod
    def handler(cls):
        variables = globals().copy()
        variables.update(locals())
        shell = code.InteractiveConsole(variables)
        shell.interact()