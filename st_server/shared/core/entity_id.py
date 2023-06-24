"""Value object that represents the entity id."""

from uuid import uuid4

from st_server.shared.core.value_object import ValueObject


class EntityId(ValueObject):
    """Value object that represents the entity id."""

    @classmethod
    def generate(cls) -> "EntityId":
        return cls(value=uuid4().hex)

    @classmethod
    def from_string(cls, value: str) -> "EntityId":
        return cls(value=value)

    def __init__(self, value: str) -> None:
        self.__dict__["value"] = value

    @property
    def value(self) -> str:
        return self.__dict__["value"]
