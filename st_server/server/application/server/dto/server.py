from dataclasses import dataclass, field

from st_server.server.application.server.dto.credential import CredentialDto
from st_server.server.application.server.dto.server_application import (
    ServerApplicationDto,
)
from st_server.server.domain.server.server import Server


@dataclass(frozen=True)
class ServerDto:
    """Data Transfer Object for reading an Server."""

    id: str
    name: str
    cpu: str
    ram: str
    hdd: str
    environment: str
    operating_system: dict
    status: str
    discarded: bool
    credentials: list[CredentialDto] = field(default_factory=list)
    applications: list[ServerApplicationDto] = field(default_factory=list)

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
                ServerApplicationDto.from_value_object(server_application)
                for server_application in server.applications
            ],
            status=server.status.value,
            discarded=server.discarded,
        )
