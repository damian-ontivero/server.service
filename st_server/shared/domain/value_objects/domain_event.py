"""Base class for domain events."""

from st_server.shared.helper.time import now


class DomainEvent:
    """Base class for domain events.

    Domain Events are value objects that represent something that happened in
    the domain. They are used to notify other parts of the application about
    something that happened in the domain.

    Attributes are specified as keyword arguments and can be added
    but not modified. This is to ensure that the domain events are immutable.
    """

    def __init__(self, **kwargs) -> None:
        """Initializes the domain event."""
        self.__dict__["occurred_on"] = now()
        self.__dict__.update(kwargs)

    def __setattr__(self, name: str, value: object) -> None:
        """Prevents setting attributes that already exist."""
        if hasattr(self, name):
            raise AttributeError("Attributes can be added but not modified")
        self.__dict__[name] = value

    def __eq__(self, other: object) -> bool:
        """Compares if two domain events are equal."""
        if isinstance(other, DomainEvent):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other: object) -> bool:
        """Compares if two domain events are not equal."""
        return not self.__eq__(other)

    def __hash__(self) -> int:
        """Returns the hash of the domain event."""
        return hash(self.__dict__)

    def __repr__(self) -> str:
        """Returns the representation of the domain event."""
        return "{c}({args})".format(
            c=self.__class__.__name__,
            args=", ".join(
                "{key}={value!r}".format(key=key, value=value)
                for key, value in self.__dict__.items()
            ),
        )
