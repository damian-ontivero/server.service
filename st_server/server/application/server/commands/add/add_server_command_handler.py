"""Contains the command handler class."""

from st_server.server.application.server.commands.add.add_server_command import (
    AddServerCommand,
)
from st_server.server.application.server.dtos.server import ServerReadDto
from st_server.server.domain.server.factories.server_factory import (
    ServerFactory,
)
from st_server.server.domain.server.repositories.server_repository import (
    ServerRepository,
)
from st_server.shared.application.commands.commad_handler import CommandHandler
from st_server.shared.application.exceptions.exception import AlreadyExists
from st_server.shared.infrastructure.message_bus.message_bus import MessageBus


class AddServerCommandHandler(CommandHandler):
    """Command handler for adding a Server."""

    def __init__(
        self, repository: ServerRepository, message_bus: MessageBus
    ) -> None:
        """Initialize the handler."""
        self._repository = repository
        self._message_bus = message_bus

    def handle(self, command: AddServerCommand) -> ServerReadDto:
        """Handle a command."""
        server = ServerFactory.build(**command.to_dict())
        self._check_exists(server.name)
        self._repository.save_one(server)
        self._message_bus.publish(server.domain_events)
        server.clear_domain_events()
        return ServerReadDto.from_entity(server)

    def _check_exists(self, name: str) -> None:
        """Returns True if a Server with the given name exists."""
        servers = self._repository.find_many(filter={"name": {"eq": name}})
        if servers.total:
            raise AlreadyExists(
                "Server with name: {name!r} already exists".format(name=name)
            )
