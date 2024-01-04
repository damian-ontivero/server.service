from dataclasses import dataclass, field

from st_server.server.application.server.dto.credential import CredentialDto
from st_server.server.application.server.dto.server_application import (
    ServerApplicationDto,
)
from st_server.server.domain.server.server import Server


@dataclass(frozen=True)
class ServerDto:
    """Data Transfer Object for reading an Server."""

    id: str | None = None
    name: str | None = None
    cpu: str | None = None
    ram: str | None = None
    hdd: str | None = None
    environment: str | None = None
    operating_system: dict | None = None
    credentials: list[CredentialDto] = field(default_factory=list)
    applications: list[ServerApplicationDto] = field(default_factory=list)
    status: str | None = None
    discarded: bool | None = None

    @classmethod
    def from_entity(cls, server: Server) -> "ServerDto":
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
                CredentialDto.from_entity(credential)
                for credential in server.credentials
            ],
            applications=[
                ServerApplicationDto.from_entity(server_application)
                for server_application in server.applications
            ],
            status=server.status.value,
            discarded=server.discarded,
        )
