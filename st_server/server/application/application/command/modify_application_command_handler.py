from st_server.server.application.application.command.modify_application_command import (
    ModifyApplicationCommand,
)
from st_server.server.application.application.dto.application import (
    ApplicationDto,
)
from st_server.server.application.domain.application_repository import (
    ApplicationRepository,
)
from st_server.shared.application.exception import AlreadyExists, NotFound
from st_server.shared.domain.bus.command.command_handler import CommandHandler
from st_server.shared.domain.bus.event.event_bus import EventBus


class ModifyApplicationCommandHandler(CommandHandler):
    def __init__(
        self, repository: ApplicationRepository, event_bus: EventBus
    ) -> None:
        self._repository = repository
        self._event_bus = event_bus

    def handle(self, command: ModifyApplicationCommand) -> ApplicationDto:
        application = self._repository.find_by_id(command.id)
        if application is None:
            raise NotFound(
                "Application with id: {id!r} not found".format(id=command.id)
            )
        if not application.name == command.name:
            self._check_if_exists(command.name)
        application.name = command.name
        application.version = command.version
        application.architect = command.architect
        self._repository.update(application)
        for domain_event in application.domain_events:
            self._message_bus.publish(domain_event)
        application.clear_domain_events()
        return ApplicationDto.from_entity(application)

    def _check_if_exists(self, name: str) -> None:
        applications = self._repository.find_many(
            filter={"name": {"eq": name}}
        )
        if applications.total:
            raise AlreadyExists(
                "Application with name: {name!r} already exists".format(
                    name=name
                )
            )
