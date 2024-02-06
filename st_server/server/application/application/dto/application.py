from dataclasses import dataclass

from st_server.server.application.domain.application import Application


@dataclass(frozen=True)
class ApplicationDto:
    id: str
    name: str
    version: str
    architect: str
    discarded: bool

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
