from st_server.server.application.application.command.discard_application_command import (
    DiscardApplicationCommand,
)
from st_server.server.application.application.command.discard_application_command_handler import (
    DiscardApplicationCommandHandler,
)
from st_server.server.application.application.command.modify_application_command import (
    ModifyApplicationCommand,
)
from st_server.server.application.application.command.modify_application_command_handler import (
    ModifyApplicationCommandHandler,
)
from st_server.server.application.application.command.register_application_command import (
    RegisterApplicationCommand,
)
from st_server.server.application.application.command.register_application_command_handler import (
    RegisterApplicationCommandHandler,
)
from st_server.server.server.application.command.discard_server_command import (
    DiscardServerCommand,
)
from st_server.server.server.application.command.discard_server_command_handler import (
    DiscardServerCommandHandler,
)
from st_server.server.server.application.command.modify_server_command import (
    ModifyServerCommand,
)
from st_server.server.server.application.command.modify_server_command_handler import (
    ModifyServerCommandHandler,
)
from st_server.server.server.application.command.register_server_command import (
    RegisterServerCommand,
)
from st_server.server.server.application.command.register_server_command_handler import (
    RegisterServerCommandHandler,
)
from st_server.shared.infrastructure.bus.command.in_memory_command_bus import (
    InMemoryCommandBus,
)
from st_server.shared.infrastructure.ui.api.dependency import (
    get_application_repository,
    get_rabbitmq_event_bus,
    get_server_repository,
)

COMMAND_HANDLER_MAPPING = {
    RegisterServerCommand: RegisterServerCommandHandler(
        repository=get_server_repository(), event_bus=get_rabbitmq_event_bus()
    ),
    ModifyServerCommand: ModifyServerCommandHandler(
        repository=get_server_repository(), event_bus=get_rabbitmq_event_bus()
    ),
    DiscardServerCommand: DiscardServerCommandHandler(
        repository=get_server_repository(), event_bus=get_rabbitmq_event_bus()
    ),
    RegisterApplicationCommand: RegisterApplicationCommandHandler(
        repository=get_application_repository(),
        event_bus=get_rabbitmq_event_bus(),
    ),
    ModifyApplicationCommand: ModifyApplicationCommandHandler(
        repository=get_application_repository(),
        event_bus=get_rabbitmq_event_bus(),
    ),
    DiscardApplicationCommand: DiscardApplicationCommandHandler(
        repository=get_application_repository(),
        event_bus=get_rabbitmq_event_bus(),
    ),
    DiscardApplicationCommand: DiscardApplicationCommandHandler(
        repository=get_application_repository(),
        event_bus=get_rabbitmq_event_bus(),
    ),
}


for command, handler in COMMAND_HANDLER_MAPPING.items():
    InMemoryCommandBus().register(command, handler)
