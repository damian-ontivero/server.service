"""Contains the command handler class."""

from st_server.server.application.server.command.add_server_command import (
    AddServerCommand,
)
from st_server.server.application.server.dto.server import ServerReadDto
from st_server.server.domain.server.server_factory import ServerFactory
from st_server.server.domain.server.server_repository import ServerRepository
from st_server.shared.application.command_handler import CommandHandler
from st_server.shared.application.exception import AlreadyExists
from st_server.shared.infrastructure.bus import Bus


class AddServerCommandHandler(CommandHandler):
    """Command handler for adding a Server."""

    def __init__(self, repository: ServerRepository, message_bus: Bus) -> None:
        """Initialize the handler."""
        self._repository = repository
        self._message_bus = message_bus

    def __call__(self, command: AddServerCommand) -> ServerReadDto:
        """Handle a command."""
        self._check_exists(command.name)
        server = ServerFactory.build(**command.to_dict())
        self._repository.save_one(server)
        self._message_bus.publish(server.domain_events)
        server.clear_domain_events()
        return ServerReadDto.from_entity(server)

    def _check_exists(self, name: str) -> None:
        """Raise an exception if a server with the given name exists."""
        servers = self._repository.find_many(filter={"name": {"eq": name}})
        if servers.total:
            raise AlreadyExists(
                "Server with name: {name!r} already exists".format(name=name)
            )
