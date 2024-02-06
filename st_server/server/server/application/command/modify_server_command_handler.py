from st_server.server.server.application.command.modify_server_command import (
    ModifyServerCommand,
)
from st_server.server.server.application.dto.server import ServerDto
from st_server.server.server.domain.environment import Environment
from st_server.server.server.domain.operating_system import OperatingSystem
from st_server.server.server.domain.server_repository import ServerRepository
from st_server.server.server.domain.server_status import ServerStatus
from st_server.shared.application.exception import AlreadyExists, NotFound
from st_server.shared.domain.bus.command.command_handler import CommandHandler
from st_server.shared.domain.bus.event.event_bus import EventBus


class ModifyServerCommandHandler(CommandHandler):
    def __init__(
        self, repository: ServerRepository, event_bus: EventBus
    ) -> None:
        self._repository = repository
        self._event_bus = event_bus

    def handle(self, command: ModifyServerCommand) -> ServerDto:
        server = self._repository.find_by_id(command.id)
        if server is None:
            raise NotFound(
                "Server with id: {id!r} not found".format(id=command.id)
            )
        if not server.name == command.name:
            self._check_if_exists(command.name)
        server.name = command.name
        server.cpu = command.cpu
        server.ram = command.ram
        server.hdd = command.hdd
        server.environment = Environment.from_text(command.environment)
        server.operating_system = OperatingSystem.from_data(
            command.operating_system
        )
        # server.credentials = command.credentials
        # server.applications = command.applications
        server.status = ServerStatus.from_text(command.status)
        self._repository.update(server)
        with self._event_bus:
            for domain_event in server.domain_events:
                self._event_bus.publish(domain_event)
        server.clear_domain_events()

    def _check_if_exists(self, name: str) -> None:
        servers = self._repository.find_many(filter={"name": {"eq": name}})
        if servers.total:
            raise AlreadyExists(
                "Server with name: {name!r} already exists".format(name=name)
            )
