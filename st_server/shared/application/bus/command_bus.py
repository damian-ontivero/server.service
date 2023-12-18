from st_server.shared.application.command import Command
from st_server.shared.application.command_handler import CommandHandler


class CommandBus:
    """Command bus dispatches commands to their handlers."""

    def __init__(self):
        self._handlers: dict[type(Command), CommandHandler] = {}

    def register(self, command: Command, handler: CommandHandler) -> None:
        """Registers a command and its handler."""
        if not isinstance(command, Command):
            raise TypeError(
                f"Invalid command type: {type(command)}. Expected type: Command"
            )
        if not isinstance(handler, CommandHandler):
            raise TypeError(
                f"Invalid handler type: {type(handler)}. Expected type: CommandHandler"
            )
        if type(command) in self._handlers:
            raise NotImplementedError(
                f"Command {type(command)} is already registered"
            )
        self._handlers[type(command)] = handler

    def dispatch(self, command: Command) -> None:
        """Dispatches a command to its handler."""
        if not isinstance(command, Command):
            raise TypeError(
                f"Invalid command type: {type(command)}. Expected type: Command"
            )
        if type(command) not in self._handlers:
            raise NotImplementedError(
                f"No registered handler found for command: {type(command)}"
            )
        handler = self._handlers[type(command)]
        handler.handle(command)
