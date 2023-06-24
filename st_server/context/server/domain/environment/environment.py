"""Environment entity.

This is the aggregate root entity of the environment aggregate.
"""

from st_server.shared.core.aggregate_root import AggregateRoot
from st_server.shared.core.domain_event import DomainEvent
from st_server.shared.core.entity_id import EntityId


class Environment(AggregateRoot):
    """Environment entity."""

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
            Do not use directly to create a new Environment.
            Use the factory method `Environment.create` instead.
        """
        super().__init__(id=id, discarded=discarded)
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._check_not_discarded()
        domain_event = Environment.NameChanged(
            aggregate_id=self._id,
            name=value,
        )
        self._name = value
        self.register_domain_event(domain_event=domain_event)

    def __repr__(self) -> str:
        return "{d}{c}(id={id!r}, name={name!r})".format(
            d="*Discarded*" if self._discarded else "",
            c=self.__class__.__name__,
            id=self._id.value,
            name=self._name,
        )

    def to_dict(self) -> dict:
        return {
            "id": self._id.value,
            "name": self._name,
            "discarded": self._discarded,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Environment":
        return cls(
            id=EntityId.from_string(value=data["id"]),
            name=data.get("name"),
            discarded=data.get("discarded"),
        )

    @classmethod
    def create(cls, name: str) -> "Environment":
        """
        Important:
            This method is only used to create a new environment.
            When creating a new environment, the id is automatically generated
            and a domain event is registered.
        """
        environment = cls(
            id=EntityId.generate(),
            name=name,
        )
        domain_event = Environment.Created(aggregate_id=environment.id)
        environment.register_domain_event(domain_event=domain_event)
        return environment

    def update(self, name: str | None = None) -> None:
        """
        Important:
            This method is only used to update a environment.
            When updating the attributes, the domain events
            are registered by setters.
        """
        if not self.name == name:
            self.name = name
        return self

    def discard(self) -> None:
        domain_event = Environment.Discarded(aggregate_id=self._id)
        self._discarded = True
        self.register_domain_event(domain_event=domain_event)
