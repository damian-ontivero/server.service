"""Server schema."""

from dataclasses import asdict, dataclass, field

from st_server.server.interface.api.schemas.application import ApplicationRead
from st_server.server.interface.api.schemas.credential import CredentialRead


@dataclass(frozen=True)
class ServerBase:
    name: str | None = None
    cpu: str | None = None
    ram: str | None = None
    hdd: str | None = None
    environment: str | None = None
    operating_system: dict | None = None
    credentials: list[CredentialRead] = field(default_factory=list)
    applications: list[ApplicationRead] = field(default_factory=list)
    status: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class ServerRead(ServerBase):
    id: str | None = None
    discarded: bool | None = None


@dataclass(frozen=True)
class ServerUpdate(ServerBase):
    pass


@dataclass(frozen=True)
class ServerCreate(ServerBase):
    pass
