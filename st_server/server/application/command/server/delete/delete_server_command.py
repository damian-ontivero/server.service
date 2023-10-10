"""Commands for the application."""

from dataclasses import dataclass

from st_server.shared.application.command.command import Command


@dataclass(frozen=True)
class DeleteServerCommand(Command):
    """Command to delete a server."""

    id: int
