"""Server Application schema."""

from dataclasses import asdict, dataclass

from st_server.server.application.dtos.application import ApplicationReadDto
from st_server.server.domain.entities.server import ServerApplication


@dataclass(frozen=True)
class ServerApplicationBase:
    server_id: str | None = None
    application_id: str | None = None
    install_dir: str | None = None
    log_dir: str | None = None
    application: ApplicationReadDto | None = None

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
class ServerApplicationReadDto(ServerApplicationBase):
    @classmethod
    def from_entity(
        cls, server_application: ServerApplication
    ) -> "ServerApplicationReadDto":
        return cls(
            server_id=server_application.server_id.value,
            application_id=server_application.application_id.value,
            install_dir=server_application.install_dir,
            log_dir=server_application.log_dir,
            application=ApplicationReadDto.from_entity(
                application=server_application.application
            ),
        )


@dataclass(frozen=True)
class ServerApplicationUpdateDto(ServerApplicationBase):
    pass


@dataclass(frozen=True)
class ServerApplicationCreateDto(ServerApplicationBase):
    pass
