"""Server schema."""

from dataclasses import asdict, dataclass


@dataclass
class ServerBase:
    name: str | None = None
    cpu: str | None = None
    ram: str | None = None
    hdd: str | None = None
    environment: str | None = None
    operating_system: str | None = None
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
