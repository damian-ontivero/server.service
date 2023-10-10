"""Commands for the application."""

from dataclasses import dataclass

from st_server.shared.application.command.command import Command


@dataclass(frozen=True)
class UpdateApplicationCommand(Command):
    """Command to update an application."""

    id: str
    name: str
    version: str
    architect: str
