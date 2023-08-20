"""Data Transfer Objects for Application."""

from dataclasses import dataclass

from st_server.server.domain.entities.application import Application


@dataclass(frozen=True)
class ApplicationBase:
    name: str | None = None
    version: str | None = None
    architect: str | None = None


@dataclass(frozen=True)
class ApplicationReadDto(ApplicationBase):
    id: str | None = None
    discarded: bool | None = None

    @classmethod
    def from_entity(cls, application: Application) -> "ApplicationReadDto":
        return cls(
            id=application.id.value,
            name=application.name,
            version=application.version,
            architect=application.architect,
            discarded=application.discarded,
        )


@dataclass(frozen=True)
class ApplicationUpdateDto(ApplicationBase):
    pass


@dataclass(frozen=True)
class ApplicationCreateDto(ApplicationBase):
    pass
