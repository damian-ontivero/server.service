from dataclasses import dataclass

from st_server.shared.domain.bus.command.command import Command


@dataclass(frozen=True)
class DiscardServerCommand(Command):
    id: int
