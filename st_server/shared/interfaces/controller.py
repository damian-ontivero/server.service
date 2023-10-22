"""Base class for all controllers."""

from abc import ABCMeta, abstractmethod

from st_server.shared.application.command import Command


class Controller(metaclass=ABCMeta):
    """Base class for all controllers."""

    @abstractmethod
    def handle(self, command: Command):
        """Handle the given command."""
        pass
