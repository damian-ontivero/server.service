"""Commands for the Application."""

from dataclasses import dataclass

from st_core.application.command import Command


@dataclass
class UpdateApplicationCommand(Command):
    """Command to update an Application."""

    id: str | None = None
    name: str | None = None
    version: str | None = None
    architect: str | None = None
