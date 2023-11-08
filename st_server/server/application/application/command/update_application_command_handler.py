"""Contains the command handler class."""

from st_server.server.application.application.command.update_application_command import (
    UpdateApplicationCommand,
)
from st_server.server.domain.application.application import Application
from st_server.server.domain.application.application_repository import (
    ApplicationRepository,
)
from st_server.shared.application.command_handler import CommandHandler
from st_server.shared.application.exception import AlreadyExists, NotFound
from st_server.shared.infrastructure.message_bus import MessageBus


class UpdateApplicationCommandHandler(CommandHandler):
    """Command handler for updating an Application."""

    def __init__(
        self, repository: ApplicationRepository, message_bus: MessageBus
    ) -> None:
        """Initialize the handler."""
        self._repository = repository
        self._message_bus = message_bus

    def handle(self, command: UpdateApplicationCommand) -> Application:
        """Handle a command."""
        application = self._repository.find_one(command.id)
        if application is None:
            raise NotFound(
                "Application with id: {id!r} not found".format(id=command.id)
            )
        if not application.name == command.name:
            self._check_if_exists(command.name)
        application.update(
            name=command.name,
            version=command.version,
            architect=command.architect,
        )
        self._repository.save_one(application)
        self._message_bus.publish(application.domain_events)
        application.clear_domain_events()
        return application

    def _check_if_exists(self, name: str) -> None:
        """Check if an Application with the given name already exists."""
        applications = self._repository.find_many(
            filter={"name": {"eq": name}}
        )
        if applications.total:
            raise AlreadyExists(
                "Application with name: {name!r} already exists".format(
                    name=name
                )
            )
