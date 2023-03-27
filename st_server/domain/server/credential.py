"""Credential entity."""

from dataclasses import dataclass, field
from datetime import datetime

from st_server.domain.connection_type import ConnectionType


@dataclass
class Credential:
    """Credential entity."""

    id: int
    server_id: int
    connection_type_id: int
    username: str
    password: str
    local_ip: str
    local_port: str
    public_ip: str | None = None
    public_port: str | None = None
    created_at: datetime = field(init=False)
    updated_at: datetime | None = field(init=False)

    connection_type: ConnectionType = field(init=False)


@dataclass
class CredentialFull:
    """Full data transfer object for Credential.

    Includes plain attributes and relationships.
    """

    id: int
    server_id: int
    connection_type_id: int
    username: str
    password: str
    local_ip: str
    local_port: str
    public_ip: str | None = None
    public_port: str | None = None
    created_at: datetime = field(init=False)
    updated_at: datetime | None = field(init=False)

    connection_type: ConnectionType = field(init=False)


@dataclass
class CredentialSimple:
    """Simple data transfer object for Credential.

    Only includes plain attributes.
    """

    id: int
    server_id: int
    connection_type_id: int
    username: str
    password: str
    local_ip: str
    local_port: str
    public_ip: str | None = None
    public_port: str | None = None
    created_at: datetime = field(init=False)
    updated_at: datetime | None = field(init=False)


@dataclass
class CredentialCreate:
    """Data transfer object to create Credential."""

    server_id: int
    connection_type_id: int
    username: str
    password: str
    local_ip: str
    local_port: str
    public_ip: str | None = None
    public_port: str | None = None


@dataclass
class CredentialUpdate:
    """Data transfer object to update a Credential."""

    id: int
    server_id: int
    connection_type_id: int
    username: str
    password: str
    local_ip: str
    local_port: str
    public_ip: str | None = None
    public_port: str | None = None
