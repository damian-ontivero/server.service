"""Value object that represents the entity id."""

from uuid import uuid4

from st_server.shared.core.value_object import ValueObject


class EntityId(ValueObject):
    """Value object that represents the entity id."""

    @classmethod
    def generate(cls) -> "EntityId":
        """Generates a new entity id.

        Important:
            This method is used to create new entity id instances.

        Returns:
            `EntityId`: New entity id.
        """
        return cls(value=uuid4().hex)

    @classmethod
    def from_string(cls, value: str) -> "EntityId":
        """Creates an entity id from string.

        Important:
            This method is used to create new entity id instance.

        Args:
            value (`str`): Entity id value.

        Returns:
            `EntityId`: New entity id instance.
        """
        return cls(value=value)

    def __init__(self, value: str) -> None:
        """Initializes a new instance of the EntityId class.

        Args:
            value (`str`): Entity id value. Defaults to None.
        """
        self.__dict__["value"] = value

    @property
    def value(self) -> str:
        """Returns the entity id value.

        Returns:
            `str`: Entity id value.
        """
        return self.__dict__["value"]
