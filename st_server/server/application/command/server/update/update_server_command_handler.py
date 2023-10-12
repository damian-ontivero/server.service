"""Contains the command handler class."""

from st_server.shared.application.command.commad_handler import CommandHandler
from st_server.shared.application.exception.exception import (
    AlreadyExists,
    NotFound,
)
from st_server.shared.infrastructure.message_bus.message_bus import MessageBus
from st_server.server.application.command.server.update.update_server_command import (
    UpdateServerCommand,
)
from st_server.server.application.dto.server import ServerReadDto
from st_server.server.domain.repository.server_repository import (
    ServerRepository,
)


class UpdateServerCommandHandler(CommandHandler):
    """Command handler for updating a server."""

    def __init__(
        self, repository: ServerRepository, message_bus: MessageBus
    ) -> None:
        """Initialize the handler."""
        self._repository = repository
        self._message_bus = message_bus

    def handle(self, command: UpdateServerCommand) -> None:
        """Handle a command."""
        server = self._repository.find_one(id=command.id)
        if server is None:
            raise NotFound(
                "Server with id: {id!r} not found".format(id=command.id)
            )
        if not server.name == command.name:
            self._check_exists(name=command.name)
        server.name = command.name or server.name
        server.cpu = command.cpu or server.cpu
        server.ram = command.ram or server.ram
        server.hdd = command.hdd or server.hdd
        server.environment = command.environment or server.environment
        server.operating_system = (
            command.operating_system or server.operating_system
        )
        server.credentials = command.credentials or server.credentials
        server.applications = command.applications or server.applications
        server.status = command.status or server.status
        self._repository.save_one(aggregate=server)
        self._message_bus.publish(domain_events=server.domain_events)
        server.clear_domain_events()
        return ServerReadDto.from_entity(server=server)

    def _check_exists(self, name: str) -> None:
        """Returns True if a server with the given name exists."""
        servers = self._repository.find_many(_filter={"name": {"eq": name}})
        if servers._total:
            raise AlreadyExists(
                "Server with name: {name!r} already exists".format(name=name)
            )
