"""Contains the command handler class."""

from st_server.server.application.application.command.delete_application_command import (
    DeleteApplicationCommand,
)
from st_server.server.application.bus.message_bus import MessageBus
from st_server.server.domain.application.application_repository import (
    ApplicationRepository,
)
from st_server.shared.application.command_handler import CommandHandler
from st_server.shared.application.exception import NotFound


class DeleteApplicationCommandHandler(CommandHandler):
    """Command handler for deleting an Application."""

    def __init__(
        self, repository: ApplicationRepository, message_bus: MessageBus
    ) -> None:
        """Initialize the handler."""
        self._repository = repository
        self._message_bus = message_bus

    def handle(self, command: DeleteApplicationCommand) -> None:
        """Handle a command."""
        application = self._repository.find_one(command.id)
        if application is None:
            raise NotFound(
                "Application with id: {id!r} not found".format(id=command.id)
            )
        self._repository.delete_one(command.id)
        self._message_bus.publish(application.domain_events)
        application.clear_domain_events()
