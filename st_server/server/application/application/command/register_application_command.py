from dataclasses import dataclass

from st_server.shared.domain.bus.command.command import Command


@dataclass(frozen=True)
class RegisterApplicationCommand(Command):
    name: str | None = None
    version: str | None = None
    architect: str | None = None
