from abc import ABCMeta, abstractmethod

from st_server.shared.domain.bus.command.command import Command
from st_server.shared.domain.bus.command.command_handler import CommandHandler


class CommandBus(metaclass=ABCMeta):
    @abstractmethod
    def register(self, command: Command, handler: CommandHandler) -> None:
        raise NotImplementedError

    @abstractmethod
    def dispatch(self, command: Command) -> None:
        raise NotImplementedError
