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
from st_server.shared.application.command_bus import BaseCommandBus
from st_server.shared.domain.repository import Repository
from st_server.shared.infrastructure.message_bus import MessageBus


class CommandBus(BaseCommandBus):
    def __init__(self, repository: Repository, message_bus: MessageBus):
        super().__init__(repository=repository, message_bus=message_bus)
        self._handlers[AddServerCommand] = AddServerCommandHandler
        self._handlers[UpdateServerCommand] = UpdateServerCommandHandler
        self._handlers[DeleteServerCommand] = DeleteServerCommandHandler
