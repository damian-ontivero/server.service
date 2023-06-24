"""Abstract base class for value objects."""

from abc import ABCMeta
from typing import Any


class ValueObject(metaclass=ABCMeta):
    """Abstract base class for value objects.

    Value objects are immutable objects that represent a concept in the domain.
    They are used to encapsulate data and behavior that belongs together.
    """

    def __setattr__(self, name: str, value: Any) -> None:
        raise AttributeError("Value objects are immutable")

    def __eq__(self, rhs: Any) -> bool:
        if not isinstance(rhs, self.__class__):
            return NotImplemented
        return self.__dict__ == rhs.__dict__

    def __ne__(self, rhs: Any) -> bool:
        return not self.__eq__(rhs)

    def __hash__(self) -> int:
        return hash(tuple(sorted(self.__dict__.items())))

    def __repr__(self) -> str:
        return (
            self.__class__.__name__
            + "("
            + ", ".join(
                "{0}={1!r}".format(k, v) for k, v in self.__dict__.items()
            )
            + ")"
        )
