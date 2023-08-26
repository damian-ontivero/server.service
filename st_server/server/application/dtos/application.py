"""Data Transfer Objects for Application."""

from dataclasses import asdict, dataclass

from st_server.server.domain.entities.application import Application


@dataclass(frozen=True)
class ApplicationBase:
    name: str | None = None
    version: str | None = None
    architect: str | None = None

    def to_dict(self, exclude_none: bool = False) -> dict:
        """Converts the DTO to a dictionary."""
        if exclude_none is True:
            return {
                key: value
                for key, value in asdict(self).items()
                if value is not None
            }
        return asdict(self)


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
