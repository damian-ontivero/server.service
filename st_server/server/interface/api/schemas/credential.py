"""Credential schema."""

from dataclasses import asdict, dataclass


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

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class CredentialRead(CredentialBase):
    id: str | None = None
    discarded: bool | None = None


@dataclass(frozen=True)
class CredentialUpdate(CredentialBase):
    pass


@dataclass(frozen=True)
class CredentialCreate(CredentialBase):
    pass
