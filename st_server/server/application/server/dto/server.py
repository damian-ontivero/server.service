"""Data Transfer Objects for Server."""

from dataclasses import dataclass, field

from st_server.server.application.server.dto.credential import (
    CredentialReadDto,
)
from st_server.server.application.server.dto.server_application import (
    ServerApplicationReadDto,
)
from st_server.server.domain.server.server import Server
from st_server.shared.application.dto import DTO


@dataclass(frozen=True)
class ServerReadDto(DTO):
    """Data Transfer Object for reading an Server."""

    id: str | None = None
    name: str | None = None
    cpu: str | None = None
    ram: str | None = None
    hdd: str | None = None
    environment: str | None = None
    operating_system: dict | None = None
    credentials: list[CredentialReadDto] = field(default_factory=list)
    applications: list[ServerApplicationReadDto] = field(default_factory=list)
    status: str | None = None
    discarded: bool | None = None

    @classmethod
    def from_entity(cls, server: Server) -> "ServerReadDto":
        """Named constructor to create a DTO from an entity."""
        return cls(
            id=server.id.value,
            name=server.name,
            cpu=server.cpu,
            ram=server.ram,
            hdd=server.hdd,
            environment=server.environment.value,
            operating_system=server.operating_system.__dict__,
            credentials=[
                CredentialReadDto.from_entity(credential)
                for credential in server.credentials
            ],
            applications=[
                ServerApplicationReadDto.from_entity(server_application)
                for server_application in server.applications
            ],
            status=server.status.value,
            discarded=server.discarded,
        )
