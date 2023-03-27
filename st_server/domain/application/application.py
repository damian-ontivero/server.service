"""Application entity."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Application:
    """Application entity."""

    id: int
    name: str
    version: str
    architect: str
    created_at: datetime = field(init=False)
    updated_at: datetime | None = field(init=False)


@dataclass
class ApplicationFull:
    """Full data transfer object for Application.

    Includes plain attributes and relationships.
    """

    id: int
    name: str
    version: str
    architect: str
    created_at: datetime = field(init=False)
    updated_at: datetime | None = field(init=False)


@dataclass
class ApplicationCreate:
    """Data transfer object to create an Application."""

    name: str
    version: str
    architect: str


@dataclass
class ApplicationUpdate:
    """Data transfer object to update an Application."""

    id: int
    name: str
    version: str
    architect: str
