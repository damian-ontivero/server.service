from dataclasses import dataclass

from st_server.server.server.domain.credential import Credential


@dataclass(frozen=True)
class CredentialDto:
    id: str
    server_id: str
    connection_type: str
    username: str
    password: str
    local_ip: str
    local_port: str
    public_ip: str
    public_port: str
    discarded: bool

    @classmethod
    def from_entity(cls, credential: Credential) -> "CredentialDto":
        """Named constructor to create a DTO from an Credential entity."""
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
