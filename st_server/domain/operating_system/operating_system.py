"""Operating System entity."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class OperatingSystem:
    """Operating System entity."""

    id: int
    name: str
    version: str
    architect: str
    created_at: datetime = field(init=False)
    updated_at: datetime | None = field(init=False)


@dataclass
class OperatingSystemFull:
    """Full data transfer object for Operating System.

    Includes plain attributes and relationships.
    """

    id: int
    name: str
    version: str
    architect: str
    created_at: datetime = field(init=False)
    updated_at: datetime | None = field(init=False)


@dataclass
class OperatingSystemCreate:
    """Data transfer object to create an Operating System."""

    name: str
    version: str
    architect: str


@dataclass
class OperatingSystemUpdate:
    """Data transfer object to update an Operating System."""

    id: int
    name: str
    version: str
    architect: str
