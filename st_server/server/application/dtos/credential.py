"""Data Transfer Objects for Credential."""

from dataclasses import asdict, dataclass

from st_server.server.domain.entities.credential import Credential


@dataclass(frozen=True)
class CredentialBase:
    server_id: str | None = None
    connection_type: str | None = None
    username: str | None = None
    password: str | None = None
    local_ip: str | None = None
    local_port: str | None = None
    public_ip: str | None = None
    public_port: str | None = None

    def to_dict(self, exclude_none: bool = False) -> dict:
        """Converts the DTO to a dictionary."""
        if exclude_none is True:
            return {
                key: value
                for key, value in asdict(self).items()
                if value is not None
            }
        return asdict(self)


@dataclass(frozen=True)
class CredentialReadDto(CredentialBase):
    id: str | None = None
    discarded: bool | None = None

    @classmethod
    def from_entity(cls, credential: Credential) -> "CredentialReadDto":
        return cls(
            id=credential.id.value,
            server_id=credential.server_id.value,
            connection_type=credential.connection_type.value,
            username=credential.username,
            password=credential.password,
            local_ip=credential.local_ip,
            local_port=credential.local_port,
            public_ip=credential.public_ip,
            public_port=credential.public_port,
            discarded=credential.discarded,
        )


@dataclass(frozen=True)
class CredentialUpdateDto(CredentialBase):
    pass


@dataclass(frozen=True)
class CredentialCreateDto(CredentialBase):
    pass
