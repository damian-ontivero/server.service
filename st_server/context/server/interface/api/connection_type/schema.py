"""ConnectionType schema."""

from dataclasses import asdict, dataclass


@dataclass
class ConnectionTypeBase:
    name: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ConnectionTypeRead(ConnectionTypeBase):
    id: str | None = None
    discarded: bool | None = None


@dataclass
class ConnectionTypeUpdate(ConnectionTypeBase):
    pass


@dataclass
class ConnectionTypeCreate(ConnectionTypeBase):
    pass
