"""Environment query parameter."""

from pydantic import BaseModel


class EnvironmentQueryParameter(BaseModel):
    """Environment query parameter."""

    id: str | None = None
    name: str | None = None
    discarded: bool | None = None
