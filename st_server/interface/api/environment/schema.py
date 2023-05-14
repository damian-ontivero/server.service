"""Environment schema."""

from dataclasses import asdict, dataclass


@dataclass
class EnvironmentBase:
    name: str | None = None

    def to_dict(self) -> dict:
        """Returns a dictionary representation of the object.

        Returns:
            `dict`: Dictionary representation of the object.
        """
        return asdict(self)


@dataclass
class EnvironmentRead(EnvironmentBase):
    id: str | None = None
    discarded: bool | None = None


@dataclass
class EnvironmentUpdate(EnvironmentBase):
    pass


@dataclass
class EnvironmentCreate(EnvironmentBase):
    pass
