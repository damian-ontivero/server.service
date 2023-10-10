"""Contains the command handler class."""

from st_server.shared.application.command.commad_handler import CommandHandler
from st_server.shared.application.exception.exception import (
    AlreadyExists,
    NotFound,
)
from st_server.shared.infrastructure.message_bus.message_bus import MessageBus
from st_server.server.application.command.application.update.update_application_command import (
    UpdateApplicationCommand,
)
from st_server.server.application.dto.application import ApplicationReadDto
from st_server.server.domain.repository.application_repository import (
    ApplicationRepository,
)


class UpdateApplicationCommandHandler(CommandHandler):
    """Command handler for updating an application."""

    def __init__(
        self, repository: ApplicationRepository, message_bus: MessageBus
    ) -> None:
        """Initialize the handler."""
        self._repository = repository
        self._message_bus = message_bus

    def handle(self, command: UpdateApplicationCommand) -> None:
        """Handle a command."""
        application = self._repository.find_one(id=command.id)
        if application is None:
            raise NotFound(
                "Application with id: {id!r} not found".format(id=command.id)
            )
        if not application.name == command.name:
            self._check_exists(name=command.name)
        application.name = command.name or application.name
        self._repository.save_one(aggregate=application)
        self._message_bus.publish(domain_events=application.domain_events)
        application.clear_domain_events()
        application = self._repository.find_one(id=command.id)
        return ApplicationReadDto.from_entity(application=application)

    def _check_exists(self, name: str) -> None:
        """Returns True if an application with the given name exists."""
        applications = self._repository.find_many(
            _filter={"name": {"eq": name}}
        )
        if applications._total:
            raise AlreadyExists(
                "Application with name: {name!r} already exists".format(
                    name=name
                )
            )
