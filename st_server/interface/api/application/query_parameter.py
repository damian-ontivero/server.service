"""Application query parameter."""

from pydantic import BaseModel


class ApplicationQueryParameter(BaseModel):
    """Application query parameter."""

    id: str | None = None
    name: str | None = None
    version: str | None = None
    architect: str | None = None
    discarded: bool | None = None
