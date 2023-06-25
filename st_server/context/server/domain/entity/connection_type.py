"""ConnectionType entity.

This is the aggregate root entity of the ConnectionType aggregate.
"""

from st_server.shared.core.aggregate_root import AggregateRoot
from st_server.shared.core.domain_event import DomainEvent
from st_server.shared.core.entity_id import EntityId


class ConnectionType(AggregateRoot):
    """ConnectionType entity."""

    class Created(DomainEvent):
        pass

    class Discarded(DomainEvent):
        pass

    class NameChanged(DomainEvent):
        pass

    def __init__(
        self,
        id: EntityId | None = None,
        name: str = None,
        discarded: bool | None = None,
    ) -> None:
        """
        Important:
            Do not use directly to create a new ConnectionType.
            Use the factory method `ConnectionType.create` instead.
        """
        super().__init__(id=id, discarded=discarded)
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._check_not_discarded()
        domain_event = ConnectionType.NameChanged(
            aggregate_id=self.id.value,
            old_value=self.name,
            new_value=value,
        )
        self._name = value
        self.register_domain_event(domain_event=domain_event)

    def __repr__(self) -> str:
        return (
            "{d}{c}(id={id!r}, name={name!r}, discarded={discarded!r})"
        ).format(
            d="*Discarded*" if self.discarded else "",
            c=self.__class__.__name__,
            id=self.id,
            name=self.name,
            discarded=self.discarded,
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id.value,
            "name": self.name,
            "discarded": self.discarded,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ConnectionType":
        return cls(
            id=EntityId.from_string(value=data.get("id")),
            name=data.get("name"),
            discarded=data.get("discarded"),
        )

    @classmethod
    def create(cls, name: str) -> "ConnectionType":
        """
        Important:
            This method is only used to create a new ConnectionType.
            When creating a new ConnectionType, the id is automatically generated
            and a domain event is registered.
        """
        connection_type = cls(
            id=EntityId.generate(),
            name=name,
        )
        domain_event = ConnectionType.Created(
            aggregate_id=connection_type.id.value
        )
        connection_type.register_domain_event(domain_event=domain_event)
        return connection_type

    def update(self, name: str | None = None) -> None:
        """
        Important:
            This method is only used to update a ConnectionType.
            When updating the attributes, the domain events
            are registered by setters.
        """
        if not self.name == name:
            self.name = name
        return self

    def discard(self) -> None:
        """
        Important:
            This method is only used to discard a ConnectionType.
            When discarding a ConnectionType, the discarded attribute is set to True
            and a domain event is registered.
        """
        domain_event = ConnectionType.Discarded(aggregate_id=self.id.value)
        self.discarded = True
        self.register_domain_event(domain_event=domain_event)
