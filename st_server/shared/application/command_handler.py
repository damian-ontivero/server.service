from abc import ABCMeta, abstractmethod

from st_server.shared.application.command import Command


class CommandHandler(metaclass=ABCMeta):
    """Abstract base class for command handlers.

    This class represents the blueprint for handling commands within the application.
    """

    @abstractmethod
    def handle(self, command: Command) -> None:
        raise NotImplementedError
