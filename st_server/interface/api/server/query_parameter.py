"""Server query parameter."""

from pydantic import BaseModel


class ServerQueryParameter(BaseModel):
    """Server query parameter."""

    id: str | None = None
    name: str | None = None
    environment_id: int | None = None
    operating_system_id: int | None = None
    cpu: str | None = None
    ram: str | None = None
    hdd: str | None = None
    discarded: bool | None = None
