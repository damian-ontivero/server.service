"""Application schema."""

from pydantic import BaseModel


class ApplicationBase(BaseModel):
    name: str | None = None
    version: str | None = None
    architect: str | None = None


class ApplicationRead(ApplicationBase):
    id: str | None = None
    discarded: bool | None = None


class ApplicationUpdate(ApplicationBase):
    pass


class ApplicationCreate(ApplicationBase):
    pass
