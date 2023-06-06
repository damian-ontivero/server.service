"""Server schema."""

from dataclasses import asdict, dataclass

from st_server.context.server.interface.api.environment.schema import (
    EnvironmentRead,
)
from st_server.context.server.interface.api.operating_system.schema import (
    OperatingSystemRead,
)


@dataclass
class ServerBase:
    name: str | None = None
    cpu: str | None = None
    ram: str | None = None
    hdd: str | None = None
    environment_id: str | None = None
    environment: EnvironmentRead | None = None
    operating_system_id: str | None = None
    operating_system: OperatingSystemRead | None = None
    credentials: list | None = None
    applications: list | None = None

    def to_dict(self) -> dict:
        """Returns a dictionary representation of the object.

        Returns:
            `dict`: Dictionary representation of the object.
        """
        return asdict(self)


@dataclass
class ServerRead(ServerBase):
    id: str | None = None
    discarded: bool | None = None


@dataclass
class ServerUpdate(ServerBase):
    pass


@dataclass
class ServerCreate(ServerBase):
    pass
