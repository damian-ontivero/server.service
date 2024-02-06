from abc import ABCMeta, abstractmethod

from st_server.shared.domain.bus.command.command import Command


class CommandHandler(metaclass=ABCMeta):
    @abstractmethod
    def handle(self, command: Command) -> None:
        raise NotImplementedError
