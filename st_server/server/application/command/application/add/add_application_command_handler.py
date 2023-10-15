"""Contains the command handler class."""

from st_server.shared.application.command.commad_handler import CommandHandler
from st_server.shared.application.exception.exception import AlreadyExists
from st_server.shared.infrastructure.message_bus.message_bus import MessageBus
from st_server.server.application.command.application.add.add_application_command import (
    AddApplicationCommand,
)
from st_server.server.application.dto.application import ApplicationReadDto
from st_server.server.domain.entity.application import Application
from st_server.server.domain.repository.application_repository import (
    ApplicationRepository,
)


class AddApplicationCommandHandler(CommandHandler):
    """Command handler for adding an application."""

    def __init__(
        self, repository: ApplicationRepository, message_bus: MessageBus
    ) -> None:
        """Initialize the handler."""
        self._repository = repository
        self._message_bus = message_bus

    def handle(self, command: AddApplicationCommand) -> ApplicationReadDto:
        """Handle a command."""
        application = Application.create(
            name=command.name,
            version=command.version,
            architect=command.architect,
        )
        self._check_exists(application.name)
        self._repository.save_one(application)
        self._message_bus.publish(application.domain_events)
        application.clear_domain_events()
        return ApplicationReadDto.from_entity(application)

    def _check_exists(self, name: str) -> None:
        """Returns True if an application with the given name exists."""
        applications = self._repository.find_many(
            filter={"name": {"eq": name}}
        )
        if applications.total:
            raise AlreadyExists(
                "Application with name: {name!r} already exists".format(
                    name=name
                )
            )
