"""Connection type query parameter."""

from pydantic import BaseModel


class ConnectionTypeQueryParameter(BaseModel):
    """Connection type query parameter."""

    id: str | None = None
    name: str | None = None
    discarded: bool | None = None
