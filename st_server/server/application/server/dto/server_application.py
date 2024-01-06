from dataclasses import dataclass

from st_server.server.domain.server.server import ServerApplication


@dataclass(frozen=True)
class ServerApplicationDto:
    """Data Transfer Object for reading an ServerApplication."""

    server_id: str
    application_id: str
    install_dir: str
    log_dir: str

    @classmethod
    def from_value_object(
        cls, server_application: ServerApplication
    ) -> "ServerApplicationDto":
        """Named constructor to create a DTO from an Server Application entity."""
        return cls(
            server_id=server_application.server_id.value,
            application_id=server_application.application_id.value,
            install_dir=server_application.install_dir,
            log_dir=server_application.log_dir,
        )
