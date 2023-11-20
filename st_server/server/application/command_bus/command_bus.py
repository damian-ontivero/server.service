from st_core.application.command import Command
from st_core.application.command_handler import CommandHandler


class CommandBus:
    """Command bus dispatches commands to their handlers."""

    def __init__(self):
        self._handlers: dict[type(Command), CommandHandler] = {}

    def register(self, command: Command, handler: CommandHandler) -> None:
        """Registers a command and its handler."""
        if not isinstance(command, Command):
            raise TypeError(f"{type(command)} is not a valid command")
        if not isinstance(handler, CommandHandler):
            raise TypeError(f"{type(handler)} is not a valid handler")
        if type(command) in self._handlers:
            raise NotImplementedError(f"{type(command)} is already registered")
        self._handlers[type(command)] = handler

    def dispatch(self, command: Command) -> None:
        """Dispatches a command to its handler."""
        if not isinstance(command, Command):
            raise TypeError(f"{type(command)} is not a valid command")
        if not type(command) in self._handlers:
            raise NotImplementedError(f"{type(command)} is not registered")
        handler = self._handlers[type(command)]
        handler.handle(command)
