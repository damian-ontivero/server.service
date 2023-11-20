"""Commands for the Server."""

from dataclasses import dataclass

from st_core.application.command import Command


@dataclass
class DeleteServerCommand(Command):
    """Command to delete a Server."""

    id: int
