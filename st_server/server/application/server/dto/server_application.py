"""Server Application schema."""

from dataclasses import dataclass

from st_server.server.application.application.dto.application import (
    ApplicationReadDto,
)
from st_server.server.domain.server.server import ServerApplication
from st_server.shared.application.dto import DTO


@dataclass(frozen=True)
class ServerApplicationReadDto(DTO):
    """Data Transfer Object for reading an ServerApplication."""

    application_id: str | None = None
    install_dir: str | None = None
    log_dir: str | None = None
    application: ApplicationReadDto | None = None

    @classmethod
    def from_entity(
        cls, server_application: ServerApplication
    ) -> "ServerApplicationReadDto":
        """Named constructor to create a DTO from an Server Application entity."""
        return cls(
            application_id=server_application.application_id.value,
            install_dir=server_application.install_dir,
            log_dir=server_application.log_dir,
            application=ApplicationReadDto.from_entity(
                server_application.application
            ),
        )
