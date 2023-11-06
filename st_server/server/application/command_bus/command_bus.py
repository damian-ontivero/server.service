from st_server.server.application.application.command.add_application_command import (
    AddApplicationCommand,
)
from st_server.server.application.application.command.add_application_command_handler import (
    AddApplicationCommandHandler,
)
from st_server.server.application.application.command.delete_application_command import (
    DeleteApplicationCommand,
)
from st_server.server.application.application.command.delete_application_command_handler import (
    DeleteApplicationCommandHandler,
)
from st_server.server.application.application.command.update_application_command import (
    UpdateApplicationCommand,
)
from st_server.server.application.application.command.update_application_command_handler import (
    UpdateApplicationCommandHandler,
)
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
from st_server.shared.domain.repository import Repository
from st_server.shared.infrastructure.message_bus import MessageBus


class CommandBus:
    """Command bus dispatches commands to their handlers."""

    def __init__(self, repository: Repository, message_bus: MessageBus):
        self._repository = repository
        self._message_bus = message_bus
        self._handlers = {
            AddServerCommand: AddServerCommandHandler,
            UpdateServerCommand: UpdateServerCommandHandler,
            DeleteServerCommand: DeleteServerCommandHandler,
            AddApplicationCommand: AddApplicationCommandHandler,
            UpdateApplicationCommand: UpdateApplicationCommandHandler,
            DeleteApplicationCommand: DeleteApplicationCommandHandler,
        }

    def dispatch(self, command: Command) -> None:
        handler_class = self._handlers.get(type(command))
        if handler_class is None:
            raise Exception(
                f"No handler registered for command {type(command).__name__}"
            )
        handler = handler_class(
            repository=self._repository, message_bus=self._message_bus
        )
        handler.handle(command)
