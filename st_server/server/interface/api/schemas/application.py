"""Application schema."""

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class ApplicationBase:
    name: str | None = None
    version: str | None = None
    architect: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class ApplicationRead(ApplicationBase):
    id: str | None = None
    discarded: bool | None = None


@dataclass(frozen=True)
class ApplicationUpdate(ApplicationBase):
    pass


@dataclass(frozen=True)
class ApplicationCreate(ApplicationBase):
    pass
