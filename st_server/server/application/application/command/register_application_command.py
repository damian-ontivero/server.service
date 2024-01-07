from dataclasses import dataclass

from st_server.shared.application.command import Command


@dataclass
class RegisterApplicationCommand(Command):
    name: str | None = None
    version: str | None = None
    architect: str | None = None