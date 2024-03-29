"""Data Transfer Objects for Server."""

from dataclasses import dataclass, field

from st_server.server.application.dtos.credential import CredentialReadDto
from st_server.server.application.dtos.server_application import (
    ServerApplicationReadDto,
)
from st_server.server.domain.entities.server import Server


@dataclass(frozen=True)
class ServerBase:
    name: str | None = None
    cpu: str | None = None
    ram: str | None = None
    hdd: str | None = None
    environment: str | None = None
    operating_system: dict | None = None
    credentials: list[CredentialReadDto] = field(default_factory=list)
    applications: list[ServerApplicationReadDto] = field(default_factory=list)
    status: str | None = None


@dataclass(frozen=True)
class ServerReadDto(ServerBase):
    id: str | None = None
    discarded: bool | None = None

    @classmethod
    def from_entity(cls, server: Server) -> "ServerReadDto":
        return cls(
            id=server.id.value,
            name=server.name,
            cpu=server.cpu,
            ram=server.ram,
            hdd=server.hdd,
            environment=server.environment.value,
            operating_system=server.operating_system.__dict__,
            credentials=[
                CredentialReadDto.from_entity(credential=credential)
                for credential in server.credentials
            ],
            applications=[
                ServerApplicationReadDto.from_entity(
                    server_application=server_application
                )
                for server_application in server.applications
            ],
            status=server.status.value,
            discarded=server.discarded,
        )


@dataclass(frozen=True)
class ServerUpdateDto(ServerBase):
    pass


@dataclass(frozen=True)
class ServerCreateDto(ServerBase):
    pass
