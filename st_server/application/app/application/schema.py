"""Application query parameters."""

from pydantic import BaseModel


class ApplicationQueryParams(BaseModel):
    """Application query parameters."""

    id: str | None = None
    name: str | None = None
    version: str | None = None
    architect: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
