"""Environment entity."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Environment:
    """Environment entity."""

    id: int
    name: str
    created_at: datetime = field(init=False)
    updated_at: datetime | None = field(init=False)


@dataclass
class EnvironmentFull:
    """Full data transfer object for Environment.

    Includes plain attributes and relationships.
    """

    id: int
    name: str
    created_at: datetime = field(init=False)
    updated_at: datetime | None = field(init=False)


@dataclass
class EnvironmentCreate:
    """Data transfer object to create an Environment."""

    name: str


@dataclass
class EnvironmentUpdate:
    """Data transfer object to update an Environment."""

    id: int
    name: str
