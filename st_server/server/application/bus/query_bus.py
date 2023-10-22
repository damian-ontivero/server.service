"""Command bus implementation."""

from st_server.server.application.server.command.add_server_command import (
    AddServerCommand,
)
from st_server.server.application.server.command.add_server_command_handler import (
    AddServerCommandHandler,
)
from st_server.server.application.server.command.delete_server_command import (
    DeleteServerCommand,
)
from st_server.server.application.server.command.delete_server_command_handler import (
    DeleteServerCommandHandler,
)
from st_server.server.application.server.command.update_server_command import (
    UpdateServerCommand,
)
from st_server.server.application.server.command.update_server_command_handler import (
    UpdateServerCommandHandler,
)
from st_server.shared.application.command import Command
from st_server.shared.application.command_handler import CommandHandler
from st_server.shared.domain.repository import Repository
from st_server.shared.infrastructure.bus import Bus


class QueryBus(Bus):
    def __init__(self, repository: Repository, message_bus: Bus):
        self._repository = repository
        self._message_bus = message_bus
        self._handlers: dict[type[Command], CommandHandler] = dict()
        self._register_handlers()

    def _register_handlers(self):
        self._handlers[AddServerCommand] = AddServerCommandHandler
        self._handlers[UpdateServerCommand] = UpdateServerCommandHandler
        self._handlers[DeleteServerCommand] = DeleteServerCommandHandler

    def dispatch(self, command: Command) -> None:
        handler = self._handlers.get(type(command))
        if handler is None:
            raise Exception("No handler registered for command")
        handler = handler(
            repository=self._repository, message_bus=self._message_bus
        )
        handler(command)

    def publish(self) -> None:
        """Publishes the domain events."""
        raise NotImplementedError
