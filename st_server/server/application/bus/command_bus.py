from st_server.server.application.command.server.add.add_server_command import (
    AddServerCommand,
)
from st_server.server.application.command.server.add.add_server_command_handler import (
    AddServerCommandHandler,
)
from st_server.server.application.command.server.delete.delete_server_command import (
    DeleteServerCommand,
)
from st_server.server.application.command.server.delete.delete_server_command_handler import (
    DeleteServerCommandHandler,
)
from st_server.server.application.command.server.update.update_server_command import (
    UpdateServerCommand,
)
from st_server.server.application.command.server.update.update_server_command_handler import (
    UpdateServerCommandHandler,
)
from st_server.shared.application.command.command import Command
from st_server.server.infrastructure.persistence.mysql.


class CommandBus:
    def __init__(self):
        self._handlers = dict()
        self._register_handlers()
        self._repository = 
        self._message_bus = 

    def _register_handlers(self):
        self._handlers[AddServerCommand] = AddServerCommandHandler
        self._handlers[UpdateServerCommand] = UpdateServerCommandHandler
        self._handlers[DeleteServerCommand] = DeleteServerCommandHandler

    def dispatch(self, command: Command):
        handler = self._handlers.get(type(command))
        if handler is None:
            raise Exception("No handler registered for command")
        handler(
            repository=self._repository, message_bus=self._message_bus
        ).handle(command)
