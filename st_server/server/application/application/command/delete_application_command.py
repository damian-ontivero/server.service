from dataclasses import dataclass

from st_server.shared.application.command import Command


@dataclass
class DeleteApplicationCommand(Command):
    """Command to delete an Application."""

    id: int
