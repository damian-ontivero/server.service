"""Environment entity.

This is the aggregate root entity of the environment aggregate.
"""

from st_server.shared.core.aggregate_root import AggregateRoot
from st_server.shared.core.domain_event import DomainEvent
from st_server.shared.core.entity_id import EntityId


class Environment(AggregateRoot):
    """Environment entity."""

    class Created(DomainEvent):
        """Domain event for Environment created."""

        pass

    class Discarded(DomainEvent):
        """Domain event for Environment discarded."""

        pass

    class NameChanged(DomainEvent):
        """Domain event for name changed."""

        pass

    def __init__(
        self,
        id: EntityId | None = None,
        name: str = None,
        discarded: bool | None = None,
    ) -> None:
        """Initializes a new instance of the Environment class.

        Important:
            This initializer should not be used directly to generate the entity.
            It should be used only by the repository to instantiate the entity from the database.

            In order to create/generate/register a new environment, use the `Environment.create` method.

        Args:
            name (`str`): Environment name.
            discarded (`bool`): Indicates if the environment is discarded.
        """
        super().__init__(id=id, discarded=discarded)
        self._name = name

    @property
    def name(self) -> str:
        """Returns the environment name.

        Returns:
            `str`: Environment name.
        """
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Sets the name of the environment.

        Args:
            value (`str`): Name of the environment.
        """
        self._check_not_discarded()

        if self._name == value:
            return

        domain_event = Environment.NameChanged(
            aggregate_id=self._id,
            name=value,
        )

        self._name = value
        self.register_domain_event(domain_event=domain_event)

    def __repr__(self) -> str:
        """Returns the string representation of the object.

        Returns:
            `str`: String representation of the object.
        """
        return "{d}{c}(id={id!r}, name={name!r})".format(
            d="*Discarded*" if self._discarded else "",
            c=self.__class__.__name__,
            id=self._id.value,
            name=self._name,
        )

    def to_dict(self) -> dict:
        """Returns a dictionary representation of the object.

        Returns:
            `dict`: Dictionary representation of the object.
        """
        return {
            "id": self._id.value,
            "name": self._name,
            "discarded": self._discarded,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Environment":
        """Returns an instance of the class based on the provided dictionary.

        Args:
            data (`dict`): Dictionary representation of the object.

        Returns:
            `Environment`: New Environment instance.
        """
        return cls(
            id=EntityId.from_string(value=data["id"]),
            name=data.get("name"),
            discarded=data.get("discarded"),
        )

    @classmethod
    def create(cls, name: str) -> "Environment":
        """Environment factory method.

        Important:
            This method is only used to create a new environment.
            When creating a new environment, the id is automatically generated
            and a domain event is registered.

        Args:
            name (`str`): Environment name.

        Returns:
            `Environment`: New Environment.
        """
        environment = cls(
            id=EntityId.generate(),
            name=name,
        )

        domain_event = Environment.Created(aggregate_id=environment.id)
        environment.register_domain_event(domain_event=domain_event)

        return environment

    def update(self, name: str | None = None) -> None:
        """Environment update method.

        Important:
            This method is only used to update a environment.
            When updating the attributes, the domain events
            are registered by setters.

        Args:
            name (`str`): Environment name.
        """
        if name is not None:
            self.name = name

        return self

    def discard(self) -> None:
        """Environment discard method.

        Important:
            This method is only used to discard a environment.
            When discarding a environment, the discarded attribute is set to True
            and a domain event is registered.
        """
        domain_event = Environment.Discarded(aggregate_id=self._id)

        self._discarded = True
        self.register_domain_event(domain_event=domain_event)
