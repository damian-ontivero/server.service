"""ConnectionType query parameter."""

from pydantic import BaseModel


class ConnectionTypeQueryParameter(BaseModel):
    """ConnectionType query parameter."""

    id: str | None = None
    name: str | None = None
    discarded: bool | None = None
