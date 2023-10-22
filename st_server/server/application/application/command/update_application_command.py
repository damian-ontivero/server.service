"""Commands for the Application."""

from dataclasses import dataclass

from st_server.shared.application.command import Command


@dataclass(frozen=True)
class UpdateApplicationCommand(Command):
    """Command to update an Application."""

    id: str
    name: str
    version: str
    architect: str
