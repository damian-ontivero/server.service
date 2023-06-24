"""Base class for domain events."""

from typing import Any

from st_server.shared.core.value_object import ValueObject
from st_server.shared.helper.time import now


class DomainEvent(ValueObject):
    """Base class for domain events.

    Domain Events are value objects that represent something that happened in
    the domain. They are used to notify other parts of the application about
    something that happened in the domain.

    Attributes are specified as keyword arguments and can be added
    but not modified. This is to ensure that the domain events are immutable.
    """

    def __init__(self, **kwargs) -> None:
        self.__dict__["occurred_on"] = now()
        self.__dict__.update(kwargs)

    def __setattr__(self, name: str, value: Any) -> None:
        if hasattr(self, name):
            raise AttributeError("Attributes can be added but not modified")
        self.__dict__[name] = value
