"""OperatingSystem schema."""

from dataclasses import asdict, dataclass


@dataclass
class OperatingSystemBase:
    name: str | None = None
    version: str | None = None
    architect: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class OperatingSystemRead(OperatingSystemBase):
    id: str | None = None
    discarded: bool | None = None


@dataclass
class OperatingSystemUpdate(OperatingSystemBase):
    pass


@dataclass
class OperatingSystemCreate(OperatingSystemBase):
    pass