"""Connection Type query parameters."""

from pydantic import BaseModel


class ConnectionTypeQueryParams(BaseModel):
    """Connection Type query parameters."""

    id: str | None = None
    name: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
