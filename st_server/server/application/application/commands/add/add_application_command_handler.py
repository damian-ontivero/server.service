"""Contains the command handler class."""

from st_server.server.application.application.commands.add.add_application_command import (
    AddApplicationCommand,
)
from st_server.server.application.application.dtos.application import (
    ApplicationReadDto,
)
from st_server.server.domain.application.factories.application_factory import (
    ApplicationFactory,
)
from st_server.server.domain.application.repositories.application_repository import (
    ApplicationRepository,
)
from st_server.shared.application.commands.commad_handler import CommandHandler
from st_server.shared.application.exceptions.exception import AlreadyExists
from st_server.shared.infrastructure.message_bus.message_bus import MessageBus


class AddApplicationCommandHandler(CommandHandler):
    """Command handler for adding an Application."""

    def __init__(
        self, repository: ApplicationRepository, message_bus: MessageBus
    ) -> None:
        """Initialize the handler."""
        self._repository = repository
        self._message_bus = message_bus

    def handle(self, command: AddApplicationCommand) -> ApplicationReadDto:
        """Handle a command."""
        application = ApplicationFactory.build(**command.to_dict())
        self._check_exists(application.name)
        self._repository.save_one(application)
        self._message_bus.publish(application.domain_events)
        application.clear_domain_events()
        return ApplicationReadDto.from_entity(application)

    def _check_exists(self, name: str) -> None:
        """Returns True if an Application with the given name exists."""
        applications = self._repository.find_many(
            filter={"name": {"eq": name}}
        )
        if applications.total:
            raise AlreadyExists(
                "Application with name: {name!r} already exists".format(
                    name=name
                )
            )
