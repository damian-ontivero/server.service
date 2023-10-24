"""Data Transfer Objects for Credential."""

from dataclasses import dataclass

from st_server.server.domain.server.credential import Credential
from st_server.shared.presentation.dto import DTO


@dataclass(frozen=True)
class CredentialReadDto(DTO):
    """Data Transfer Object for reading an Credential."""

    id: str | None = None
    # server_id: str | None = None
    connection_type: str | None = None
    username: str | None = None
    password: str | None = None
    local_ip: str | None = None
    local_port: str | None = None
    public_ip: str | None = None
    public_port: str | None = None
    discarded: bool | None = None

    @classmethod
    def from_entity(cls, credential: Credential) -> "CredentialReadDto":
        """Named constructor to create a DTO from an Credential entity."""
        return cls(
            id=credential.id.value,
            connection_type=credential.connection_type.value,
            username=credential.username,
            password=credential.password,
            local_ip=credential.local_ip,
            local_port=credential.local_port,
            public_ip=credential.public_ip,
            public_port=credential.public_port,
            discarded=credential.discarded,
        )
