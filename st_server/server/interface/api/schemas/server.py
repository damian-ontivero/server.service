"""Server schema."""

from pydantic import BaseModel, Field

from st_server.server.interface.api.schemas.application import ApplicationRead
from st_server.server.interface.api.schemas.credential import CredentialRead


class ServerBase(BaseModel):
    name: str | None = None
    cpu: str | None = None
    ram: str | None = None
    hdd: str | None = None
    environment: str | None = None
    operating_system: dict | None = None
    credentials: list[CredentialRead] = Field(default_factory=list)
    applications: list[ApplicationRead] = Field(default_factory=list)
    status: str | None = None


class ServerRead(ServerBase):
    id: str | None = None
    discarded: bool | None = None


class ServerUpdate(ServerBase):
    pass


class ServerCreate(ServerBase):
    pass
