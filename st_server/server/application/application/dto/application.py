"""Data Transfer Objects for Application."""

from dataclasses import dataclass

from st_server.server.domain.application.application import Application
from st_server.shared.application.dto import DTO


@dataclass(frozen=True)
class ApplicationDto(DTO):
    """Data Transfer Object for reading an Application."""

    id: str | None = None
    name: str | None = None
    version: str | None = None
    architect: str | None = None
    discarded: bool | None = None

    @classmethod
    def from_entity(cls, application: Application) -> "ApplicationDto":
        """Named constructor to create a DTO from an entity."""
        return cls(
            id=application.id.value,
            name=application.name,
            version=application.version,
            architect=application.architect,
            discarded=application.discarded,
        )
