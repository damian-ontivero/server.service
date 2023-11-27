"""Contains the command handler class."""

from st_core.application.command_handler import CommandHandler
from st_core.application.exception import AlreadyExists
from st_core.application.message_bus import MessageBus

from st_server.server.application.application.command.add_application_command import (
    AddApplicationCommand,
)
from st_server.server.application.application.dto.application import (
    ApplicationDto,
)
from st_server.server.domain.application.application_factory import (
    ApplicationFactory,
)
from st_server.server.domain.application.application_repository import (
    ApplicationRepository,
)


class AddApplicationCommandHandler(CommandHandler):
    """Command handler for adding an Application."""

    def __init__(
        self, repository: ApplicationRepository, message_bus: MessageBus
    ) -> None:
        """Initialize the handler."""
        self._repository = repository
        self._message_bus = message_bus

    def handle(self, command: AddApplicationCommand) -> ApplicationDto:
        """Handle a command."""
        application = ApplicationFactory.build(**command.to_dict())
        self._check_if_exists(application.name)
        self._repository.save_one(application)
        for domain_event in application.domain_events:
            self._message_bus.publish(domain_event)
        application.clear_domain_events()
        return ApplicationDto.from_entity(application)

    def _check_if_exists(self, name: str) -> None:
        """Check if an Application with the given name already exists"""
        applications = self._repository.find_many(
            filter={"name": {"eq": name}}
        )
        if applications.total:
            raise AlreadyExists(
                "Application with name: {name!r} already exists".format(
                    name=name
                )
            )
