"""Data Transfer Objects for Application."""

from dataclasses import asdict, dataclass

from st_server.server.domain.entity.application import Application


@dataclass(frozen=True)
class ApplicationBase:
    """Base Data Transfer Object for Application."""

    name: str | None = None
    version: str | None = None
    architect: str | None = None

    def to_dict(self) -> dict:
        """Converts the DTO to a dictionary."""
        return asdict(self)


@dataclass(frozen=True)
class ApplicationReadDto(ApplicationBase):
    """Data Transfer Object for reading an Application."""

    id: str | None = None
    discarded: bool | None = None

    @classmethod
    def from_entity(cls, application: Application) -> "ApplicationReadDto":
        """Named constructor to create a DTO from an Application entity."""
        return cls(
            id=application.id.value,
            name=application.name,
            version=application.version,
            architect=application.architect,
            discarded=application.discarded,
        )


@dataclass(frozen=True)
class ApplicationUpdateDto(ApplicationBase):
    """Data Transfer Object for updating an Application."""


@dataclass(frozen=True)
class ApplicationCreateDto(ApplicationBase):
    """Data Transfer Object for creating an Application."""
