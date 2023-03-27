"""Server query parameters."""

from pydantic import BaseModel


class ServerQueryParams(BaseModel):
    """Server query parameters."""

    id: str | None = None
    name: str | None = None
    environment_id: int | None = None
    operating_system_id: int | None = None
    cpu: str | None = None
    ram: str | None = None
    hdd: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
