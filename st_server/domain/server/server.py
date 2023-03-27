"""Server entity."""

from dataclasses import dataclass, field
from datetime import datetime

from st_server.domain.environment import Environment, EnvironmentFull
from st_server.domain.operating_system import (
    OperatingSystem,
    OperatingSystemFull,
)
from st_server.domain.server import Credential, CredentialFull
from st_server.domain.server.server_application import (
    ServerApplication,
    ServerApplicationFull,
)


@dataclass
class Server:
    """Server entity."""

    id: int
    name: str
    environment_id: int
    operating_system_id: int
    cpu: str
    ram: str
    hdd: str
    created_at: datetime = field(init=False)
    updated_at: datetime | None = field(init=False)

    environment: Environment = field(init=False)
    operating_system: OperatingSystem = field(init=False)
    credentials: list[Credential] = field(default_factory=list)
    applications: list[ServerApplication] = field(default_factory=list)


@dataclass
class ServerFull:
    """Full data transfer object for Server.

    Includes plain attributes and relationships.
    """

    id: int
    name: str
    environment_id: int
    operating_system_id: int
    cpu: str
    ram: str
    hdd: str
    created_at: datetime = field(init=False)
    updated_at: datetime | None = field(init=False)

    environment: EnvironmentFull = field(init=False)
    operating_system: OperatingSystemFull = field(init=False)
    credentials: list[CredentialFull] = field(default_factory=list)
    applications: list[ServerApplicationFull] = field(default_factory=list)


@dataclass
class ServerSimple:
    """Simple data transfer object for Server.

    Only includes plain attributes.
    """

    id: int
    name: str
    environment_id: int
    operating_system_id: int
    cpu: str
    ram: str
    hdd: str
    created_at: datetime = field(init=False)
    updated_at: datetime | None = field(init=False)


@dataclass
class ServerCreate:
    """Data transfer object to create a Server."""

    name: str
    environment_id: int
    operating_system_id: int
    cpu: str
    ram: str
    hdd: str


@dataclass
class ServerUpdate:
    """Data transfer object to update a Server."""

    id: int
    name: str
    environment_id: int
    operating_system_id: int
    cpu: str
    ram: str
    hdd: str
