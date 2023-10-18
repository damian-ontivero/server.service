"""Commands for the Server."""

from dataclasses import dataclass

from st_server.shared.application.commands.command import Command


@dataclass(frozen=True)
class AddServerCommand(Command):
    """Command to add a Server."""

    name: str
    cpu: str
    ram: str
    hdd: str
    environment: dict
    operating_system: dict
    credentials: list[dict]
    applications: list[dict]
