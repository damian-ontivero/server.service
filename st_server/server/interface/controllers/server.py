from st_server.shared.application.command.command import Command
from st_server.shared.interfaces.controllers.controller import Controller


class ServerController(Controller):
    def __call__(self, command: Command):
        