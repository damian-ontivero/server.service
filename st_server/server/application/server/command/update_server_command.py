"""Commands for the Server."""

from dataclasses import dataclass

from st_server.shared.application.command import Command


@dataclass(frozen=True)
class UpdateServerCommand(Command):
    """Command to update a Server."""

    id: str
    name: str
    cpu: str
    ram: str
    hdd: str
    environment: dict
    operating_system: dict
    credentials: list[dict]
    applications: list[dict]
    status: str
