from st_server.server.application.server.command.delete_server_command import (
    DeleteServerCommand,
)
from st_server.server.domain.server.server_repository import ServerRepository
from st_server.shared.application.bus.message_bus import MessageBus
from st_server.shared.application.command_handler import CommandHandler
from st_server.shared.application.exception import NotFound


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
        server = self._repository.find_by_id(command.id)
        if server is None:
            raise NotFound(
                "Server with id: {id!r} not found".format(id=command.id)
            )
        self._repository.delete_by_id(command.id)
        for domain_event in server.domain_events:
            self._message_bus.publish(domain_event)
        server.clear_domain_events()
