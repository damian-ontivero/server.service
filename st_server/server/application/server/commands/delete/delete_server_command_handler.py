"""Contains the command handler class."""

from st_server.server.application.server.commands.delete.delete_server_command import (
    DeleteServerCommand,
)
from st_server.server.domain.server.repositories.server_repository import (
    ServerRepository,
)
from st_server.shared.application.commands.commad_handler import CommandHandler
from st_server.shared.application.exceptions.exception import NotFound
from st_server.shared.infrastructure.message_bus.message_bus import MessageBus


class DeleteServerCommandHandler(CommandHandler):
    """Command handler for deleting a Server."""

    def __init__(
        self, repository: ServerRepository, message_bus: MessageBus
    ) -> None:
        """Initialize the handler."""
        self._repository = repository
        self._message_bus = message_bus

    def handle(self, command: DeleteServerCommand) -> None:
        """Handle a command."""
        server = self._repository.find_one(command.id)
        if server is None:
            raise NotFound(
                "Server with id: {id!r} not found".format(id=command.id)
            )
        self._repository.delete_one(command.id)
        self._message_bus.publish(server.domain_events)
        server.clear_domain_events()