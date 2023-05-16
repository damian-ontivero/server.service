"""Base class for domain events."""

from typing import Any

from st_server.shared.helper import now


class DomainEvent:
    """Base class for domain events.

    Domain Events represent something that happened in the domain. They are
    used to notify other parts of the application about something that
    happened in the domain.

    Attributes are specified as keyword arguments and can be added
    but not modified. This is to ensure that the domain events are immutable.
    """

    def __init__(self, **kwargs) -> None:
        """Initializes the domain event.

        Args:
            **kwargs: Arbitrary keyword arguments.
        """
        self.__dict__["occurred_on"] = now()
        self.__dict__.update(kwargs)

    def __setattr__(self, name: str, value: Any) -> None:
        """Sets an attribute.

        Args:
            name (`str`): Attribute name.
            value (`Any`): Attribute value.

        Raises:
            `AttributeError`: If the attribute already exists.
        """
        if hasattr(self, name):
            raise AttributeError("Attributes can be added but not modified")

        self.__dict__[name] = value

    def __eq__(self, other: Any) -> bool:
        """Compares two objects based on their attributes.

        Args:
            other (`Any`): Object to compare.

        Returns:
            `bool`: True if both objects are equal.
        """
        if type(self) is not type(other):
            return NotImplemented

        return self.__dict__ == other.__dict__

    def __hash__(self) -> int:
        """Returns the hash value of the object.

        Returns:
            `int`: Hash value of the object.
        """
        return hash(tuple(sorted(self.__dict__.items())))

    def __repr__(self) -> str:
        """Returns a string representation of the object.

        Returns:
            `str`: String representation of the object.
        """
        return (
            self.__class__.__name__
            + "("
            + ", ".join(
                "{0}={1!r}".format(k, v) for k, v in self.__dict__.items()
            )
            + ")"
        )
