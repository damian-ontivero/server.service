"""Environment entity.

This is the aggregate root entity of the environment aggregate.
"""

from st_server.shared.aggregate_root import AggregateRoot
from st_server.shared.domain_event import DomainEvent
from st_server.shared.entity_id import EntityId


class Environment(AggregateRoot):
    """Environment entity."""

    class NameChanged(DomainEvent):
        """Domain event for name changed."""

        pass

    def __init__(
        self,
        id: EntityId | None = None,
        name: str = None,
        discarded: bool | None = None,
    ) -> None:
        """Constructor of the environment entity.

        Important:
            This constructor should not be used directly to generate the entity.
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
        if self._name == value:
            return

        domain_event = Environment.NameChanged(
            type_="environment_updated",
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
        return "{d}{c}(name={name!r})".format(
            d="*Discarded*" if self._discarded else "",
            c=self.__class__.__name__,
            name=self._name,
        )

    def to_dict(self) -> dict:
        """Returns a dictionary representation of the object.

        Returns:
            `dict`: Dictionary representation of the object.
        """
        return {
            "id": self.id,
            "name": self._name,
            "discarded": self._discarded,
        }

    @staticmethod
    def from_dict(data: dict) -> "Environment":
        """Returns an instance of the class based on the provided dictionary.

        Args:
            data (`dict`): Dictionary representation of the object.

        Returns:
            `Environment`: Instance of the class.
        """
        return Environment(**data)

    @staticmethod
    def create(name: str) -> "Environment":
        """Environment factory method.

        Important:
            This method is only used to create a new environment.
            When creating a new environment, the id is automatically generated
            and a domain event is registered.

        Args:
            name (`str`): Environment name.

        Returns:
            `Environment`: Environment instance.
        """
        environment = Environment(
            id=EntityId().value,
            name=name,
        )

        domain_event = Environment.Created(
            type_="environment_created", aggregate_id=environment.id
        )
        environment.register_domain_event(domain_event=domain_event)

        return environment

    def discard(self) -> None:
        """Environment discard method.

        Important:
            This method is only used to discard a environment.
            When discarding a environment, the discarded attribute is set to True
            and a domain event is registered.
        """
        domain_event = Environment.Discarded(
            type_="environment_discarded", aggregate_id=self._id
        )

        self._discarded = True
        self.register_domain_event(domain_event=domain_event)
