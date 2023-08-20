"""Server query parameter."""

from pydantic import BaseModel


class ServerQueryParameter(BaseModel):
    """Server query parameter."""

    id: str | None = None
    name: str | None = None
    environment: str | None = None
    operating_system: dict | None = None
    cpu: str | None = None
    ram: str | None = None
    hdd: str | None = None
    discarded: bool | None = None
