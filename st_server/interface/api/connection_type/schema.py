"""Connection type schema."""

from dataclasses import asdict, dataclass


@dataclass
class ConnectionTypeBase:
    name: str | None = None

    def to_dict(self) -> dict:
        """Returns a dictionary representation of the object.

        Returns:
            `dict`: Dictionary representation of the object.
        """
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
