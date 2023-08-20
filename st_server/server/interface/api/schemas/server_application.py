"""Server Application schema."""

from dataclasses import asdict, dataclass

from st_server.server.interface.api.schemas.application import ApplicationRead


@dataclass(frozen=True)
class ServerApplicationBase:
    server_id: str | None = None
    application_id: str | None = None
    install_dir: str | None = None
    log_dir: str | None = None
    application: ApplicationRead | None = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class ServerApplicationRead(ServerApplicationBase):
    pass


@dataclass(frozen=True)
class ServerApplicationUpdateDto(ServerApplicationBase):
    pass


@dataclass(frozen=True)
class ServerApplicationCreateDto(ServerApplicationBase):
    pass
