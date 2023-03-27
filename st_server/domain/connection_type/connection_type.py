"""Connection Type entity."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ConnectionType:
    """Connection Type entity."""

    id: int
    name: str
    created_at: datetime = field(init=False)
    updated_at: datetime | None = field(init=False)


@dataclass
class ConnectionTypeFull:
    """Full data transfer object for Connection Type.

    Includes plain attributes and relationships.
    """

    id: int
    name: str
    created_at: datetime = field(init=False)
    updated_at: datetime | None = field(init=False)


@dataclass
class ConnectionTypeCreate:
    """Data transfer object to create a Connection Type."""

    name: str


@dataclass
class ConnectionTypeUpdate:
    """Data transfer object to update a Connection Type."""

    id: int
    name: str
