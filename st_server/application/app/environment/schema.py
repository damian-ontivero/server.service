"""Environment query parameters."""

from pydantic import BaseModel


class EnvironmentQueryParams(BaseModel):
    """Environment query parameters."""

    id: str | None = None
    name: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
