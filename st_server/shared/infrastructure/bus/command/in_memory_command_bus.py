from typing import Dict

from st_server.shared.domain.bus.command.command import Command
from st_server.shared.domain.bus.command.command_bus import CommandBus
from st_server.shared.domain.bus.command.command_handler import CommandHandler


class InMemoryCommandBus(CommandBus):
    _instance = None

    def __new__(cls) -> "InMemoryCommandBus":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._handlers: Dict[Command, CommandHandler] = {}
        return cls._instance

    def register(self, command: Command, handler: CommandHandler) -> None:
        if not issubclass(command, Command):
            raise TypeError(
                f"Invalid command type: {command.__class__.__name__}. Expected type: Command"
            )
        if not isinstance(handler, CommandHandler):
            raise TypeError(
                f"Invalid handler type: {handler.__class__.__name__}. Expected type: CommandHandler"
            )
        if type(command) in self._handlers:
            raise NotImplementedError(
                f"Command {type(command)} is already registered"
            )
        self._handlers[command] = handler

    def dispatch(self, command: Command):
        if not isinstance(command, Command):
            raise TypeError(
                f"Invalid command type: {command.__class__.__name__}. Expected type: Command"
            )
        if type(command) not in self._handlers:
            raise NotImplementedError(
                f"No registered handler found for command: {command.__class__.__name__}"
            )
        handler = self._handlers[type(command)]
        return handler.handle(command)
