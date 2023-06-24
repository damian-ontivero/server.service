"""Application schema."""

from dataclasses import asdict, dataclass


@dataclass
class ApplicationBase:
    name: str | None = None
    version: str | None = None
    architect: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ApplicationRead(ApplicationBase):
    id: str | None = None
    discarded: bool | None = None


@dataclass
class ApplicationUpdate(ApplicationBase):
    pass


@dataclass
class ApplicationCreate(ApplicationBase):
    pass
