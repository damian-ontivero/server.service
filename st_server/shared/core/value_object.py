"""Abstract base class for value objects."""

from abc import ABCMeta
from typing import Any


class ValueObject(metaclass=ABCMeta):
    """Abstract base class for value objects.

    Value objects are immutable objects that represent a concept in the domain.
    They are used to encapsulate data and behavior that belongs together.
    """

    def __setattr__(self, name: str, value: Any) -> None:
        """Sets an attribute.

        Args:
            name (`str`): Attribute name.
            value (`Any`): Attribute value.

        Raises:
            `AttributeError`: Always raised.
        """
        raise AttributeError("Value objects are immutable")

    def __eq__(self, rhs: Any) -> bool:
        """Compares two objects based on their values.

        Args:
            rhs (`Any`): Right hand side object to compare.

        Returns:
            `bool`: True if both objects are equal.
        """
        if not isinstance(rhs, self.__class__):
            return NotImplemented

        return self.__dict__ == rhs.__dict__

    def __ne__(self, rhs: Any) -> bool:
        """Compares two objects based on their values.

        Args:
            rhs (`Any`): Right hand side object to compare.

        Returns:
            `bool`: True if both objects are not equal.
        """
        return not self.__eq__(rhs)

    def __hash__(self) -> int:
        """Returns the hash value of the object.

        Returns:
            `int`: Hash value.
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
