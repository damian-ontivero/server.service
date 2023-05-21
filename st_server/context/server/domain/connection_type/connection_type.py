"""ConnectionType entity.

This is the aggregate root entity of the ConnectionType aggregate.
"""

from st_server.shared.core.aggregate_root import AggregateRoot
from st_server.shared.core.domain_event import DomainEvent
from st_server.shared.core.entity_id import EntityId


class ConnectionType(AggregateRoot):
    """ConnectionType entity."""

    class NameChanged(DomainEvent):
        """Domain event for name changed."""

        pass

    def __init__(
        self,
        id: EntityId | None = None,
        name: str = None,
        discarded: bool | None = None,
    ) -> None:
        """Constructor of the ConnectionType entity.

        Important:
            This constructor should not be used directly to generate the entity.
            It should be used only by the repository to instantiate the entity from the database.

            In order to create/generate/register a new ConnectionType, use the `ConnectionType.create` method.

        Args:
            name (`str`): ConnectionType name.
            discarded (`bool`): Indicates if the ConnectionType is discarded.
        """
        super().__init__(id=id, discarded=discarded)
        self._name = name

    @property
    def name(self) -> str:
        """Returns the ConnectionType name.

        Returns:
            `str`: ConnectionType name.
        """
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Sets the name of the ConnectionType.

        Args:
            value (`str`): Name of the ConnectionType.
        """
        if self._name == value:
            return

        domain_event = ConnectionType.NameChanged(
            type_="updated",
            aggregate_id=self.id,
            old_value=self._name,
            new_value=value,
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
    def from_dict(data: dict) -> "ConnectionType":
        """Returns an instance of the class based on the provided dictionary.

        Args:
            data (`dict`): Dictionary representation of the object.

        Returns:
            `ConnectionType`: New ConnectionType instance.
        """
        return ConnectionType(**data)

    @staticmethod
    def create(name: str) -> "ConnectionType":
        """ConnectionType factory method.

        Important:
            This method is only used to create a new ConnectionType.
            When creating a new ConnectionType, the id is automatically generated
            and a domain event is registered.

        Args:
            name (`str`): ConnectionType name.

        Returns:
            `ConnectionType`: New ConnectionType instance.
        """
        connection_type = ConnectionType(
            id=EntityId().value,
            name=name,
        )

        domain_event = ConnectionType.Created(
            type_="created", aggregate_id=connection_type.id
        )
        connection_type.register_domain_event(domain_event=domain_event)

        return connection_type

    def discard(self) -> None:
        """ConnectionType discard method.

        Important:
            This method is only used to discard a ConnectionType.
            When discarding a ConnectionType, the discarded attribute is set to True
            and a domain event is registered.
        """
        domain_event = ConnectionType.Discarded(
            type_="discarded", aggregate_id=self._id
        )

        self._discarded = True
        self.register_domain_event(domain_event=domain_event)
