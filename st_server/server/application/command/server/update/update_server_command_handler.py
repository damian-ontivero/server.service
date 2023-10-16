"""Contains the command handler class."""

from itertools import zip_longest
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
from st_server.server.domain.value_object.environment import Environment
from st_server.server.domain.value_object.operating_system import (
    OperatingSystem,
)
from st_server.server.domain.value_object.server_status import ServerStatus
from st_server.server.domain.entity.credential import Credential
from st_server.server.domain.entity.server import Server
from st_server.server.domain.entity.application import Application


class UpdateServerCommandHandler(CommandHandler):
    """Command handler for updating a server."""

    def __init__(
        self, repository: ServerRepository, message_bus: MessageBus
    ) -> None:
        """Initialize the handler."""
        self._repository = repository
        self._message_bus = message_bus

    def handle(self, command: UpdateServerCommand) -> ServerReadDto:
        """Handle a command."""
        server = self._repository.find_one(command.id)
        if server is None:
            raise NotFound(
                "Server with id: {id!r} not found".format(id=command.id)
            )
        if not server.name == command.name:
            self._check_exists(command.name)
        server.update(
            name=command.name,
            cpu=command.cpu,
            ram=command.ram,
            hdd=command.hdd,
            environment=command.environment,
            operating_system=command.operating_system,
            credentials=[
                credential.to_dict() for credential in command.credentials
            ],
            applications=[
                application.to_dict() for application in command.applications
            ],
            status=command.status,
        )
        self._repository.save_one(server)
        self._message_bus.publish(server.domain_events)
        server.clear_domain_events()
        return ServerReadDto.from_entity(server)

    def _check_exists(self, name: str) -> None:
        """Returns True if a server with the given name exists."""
        servers = self._repository.find_many(filter={"name": {"eq": name}})
        if servers.total:
            raise AlreadyExists(
                "Server with name: {name!r} already exists".format(name=name)
            )
