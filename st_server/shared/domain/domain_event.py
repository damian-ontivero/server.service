from datetime import datetime


class DomainEvent:
    """
    Base class for domain event.

    Domain events are value objects that represent something that happened in
    the domain. They are used to notify other parts of the application about
    something that happened in the domain.

    Attributes are specified as keyword arguments and can be added
    but not modified. This is to ensure that the domain event are immutable.
    """

    def __init__(self, **kwargs) -> None:
        self.__dict__["occurred_on"] = datetime.utcnow().isoformat()
        self.__dict__.update(kwargs)

    def __setattr__(self, name: str, value: object) -> None:
        """Prevents setting attributes that already exist."""
        if hasattr(self, name):
            raise AttributeError("Attributes can be added but not modified")
        self.__dict__[name] = value

    def __delattr__(self, name: str) -> None:
        """Prevents deleting attributes."""
        raise AttributeError("Attributes can be added but not deleted")

    def __eq__(self, other: object) -> bool:
        if isinstance(other, DomainEvent):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash(frozenset(self.__dict__.items()))

    def __repr__(self) -> str:
        return "{c}({args})".format(
            c=self.__class__.__name__,
            args=", ".join(
                "{key}={value!r}".format(key=key, value=value)
                for key, value in self.__dict__.items()
            ),
        )
