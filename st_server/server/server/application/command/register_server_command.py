from dataclasses import dataclass, field

from st_server.shared.domain.bus.command.command import Command


@dataclass(frozen=True)
class RegisterServerCommand(Command):
    name: str | None = None
    cpu: str | None = None
    ram: str | None = None
    hdd: str | None = None
    environment: str | None = None
    operating_system: dict | None = None
    credentials: list[dict] = field(default_factory=list)
    applications: list[dict] = field(default_factory=list)
