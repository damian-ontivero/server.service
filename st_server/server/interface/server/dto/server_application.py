"""Server Application schema."""

from dataclasses import dataclass

from st_server.server.domain.server.server import ServerApplication
from st_server.server.interface.application.dto.application import (
    ApplicationDto,
)
from st_server.shared.interface.dto import DTO


@dataclass(frozen=True)
class ServerApplicationDto(DTO):
    """Data Transfer Object for reading an ServerApplication."""

    application_id: str | None = None
    install_dir: str | None = None
    log_dir: str | None = None
    application: ApplicationDto | None = None

    @classmethod
    def from_entity(
        cls, server_application: ServerApplication
    ) -> "ServerApplicationDto":
        """Named constructor to create a DTO from an Server Application entity."""
        return cls(
            application_id=server_application.application_id.value,
            install_dir=server_application.install_dir,
            log_dir=server_application.log_dir,
            application=ApplicationDto.from_entity(
                server_application.application
            ),
        )
