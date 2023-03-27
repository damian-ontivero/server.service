"""Server Application entity."""

from dataclasses import dataclass, field

from st_server.domain.application import Application, ApplicationFull


@dataclass
class ServerApplication:
    """Server Application entity."""

    server_id: int
    application_id: int
    install_dir: str | None = None
    log_dir: str | None = None

    application: Application = field(init=False)


@dataclass
class ServerApplicationFull:
    """Full data transfer object for Server Application.

    Includes plain attributes and relationships.
    """

    server_id: int
    application_id: int
    install_dir: str | None = None
    log_dir: str | None = None

    application: ApplicationFull = field(init=False)
