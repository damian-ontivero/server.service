"""Base class for aggregate roots."""

from st_server.shared.domain.entity.entity import Entity
from st_server.shared.domain.value_object.domain_event import DomainEvent
from st_server.shared.domain.value_object.entity_id import EntityId


class AggregateRoot(Entity):
    """Base class for aggregate roots.

    Aggregate roots are entities that encapsulate a group of entities
    and value objects. They are the only entities that can be accessed
    from outside the aggregate. This is to ensure that the aggregate
    is always in a consistent state. They contain the domain events
    that are raised by the aggregate.
    """

    def __init__(self, id: EntityId, discarded: bool = False) -> None:
        """Initializes the aggregate root."""
        super().__init__(id=id, discarded=discarded)
        self._domain_events: list[DomainEvent] = []

    @property
    def domain_events(self) -> list[DomainEvent]:
        """Returns the domain events raised by the aggregate."""
        return self._domain_events

    def register_domain_event(self, domain_event: DomainEvent) -> None:
        """Registers a domain event raised by the aggregate."""
        self._domain_events.append(domain_event)

    def clear_domain_events(self) -> None:
        """Clears the domain events raised by the aggregate."""
        self._domain_events.clear()
