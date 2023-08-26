"""Server Application schema."""

from pydantic import BaseModel

from st_server.server.interface.api.schemas.application import ApplicationRead


class ServerApplicationBase(BaseModel):
    server_id: str | None = None
    application_id: str | None = None
    install_dir: str | None = None
    log_dir: str | None = None
    application: ApplicationRead | None = None


class ServerApplicationRead(ServerApplicationBase):
    pass


class ServerApplicationUpdateDto(ServerApplicationBase):
    pass


class ServerApplicationCreateDto(ServerApplicationBase):
    pass
