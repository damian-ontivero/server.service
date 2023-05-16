"""Connection type entity.

This is the aggregate root entity of the connection type aggregate.
"""

from st_server.shared.aggregate_root import AggregateRoot
from st_server.shared.domain_event import DomainEvent
from st_server.shared.entity_id import EntityId


class ConnectionType(AggregateRoot):
    """Connection type entity."""

    class NameChanged(DomainEvent):
        """Domain event for name changed."""

        pass

    def __init__(
        self,
        id: EntityId | None = None,
        name: str = None,
        discarded: bool | None = None,
    ) -> None:
        """Constructor of the connection type entity.

        Important:
            This constructor should not be used directly to generate the entity.
            It should be used only by the repository to instantiate the entity from the database.

            In order to create/generate/register a new connection type, use the `ConnectionType.create` method.

        Args:
            name (`str`): Connection type name.
            discarded (`bool`): Indicates if the connection type is discarded.
        """
        super().__init__(id=id, discarded=discarded)
        self._name = name

    @property
    def name(self) -> str:
        """Returns the connection type name.

        Returns:
            `str`: Connection type name.
        """
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Sets the name of the connection type.

        Args:
            value (`str`): Name of the connection type.
        """
        if self._name == value:
            return

        domain_event = ConnectionType.NameChanged(
            type_="connection_type_updated",
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
            `ConnectionType`: Instance of the class.
        """
        return ConnectionType(**data)

    @staticmethod
    def create(name: str) -> "ConnectionType":
        """Connection type factory method.

        Important:
            This method is only used to create a new connection type.
            When creating a new connection type, the id is automatically generated
            and a domain event is registered.

        Args:
            name (`str`): Connection type name.

        Returns:
            `ConnectionType`: Connection type instance.
        """
        connection_type = ConnectionType(
            id=EntityId().value,
            name=name,
        )

        domain_event = ConnectionType.Created(
            type_="connection_type_created", aggregate_id=connection_type.id
        )
        connection_type.register_domain_event(domain_event=domain_event)

        return connection_type

    def discard(self) -> None:
        """Connection type discard method.

        Important:
            This method is only used to discard a connection type.
            When discarding a connection type, the discarded attribute is set to True
            and a domain event is registered.
        """
        domain_event = ConnectionType.Discarded(
            type_="connection_type_discarded", aggregate_id=self._id
        )

        self._discarded = True
        self.register_domain_event(domain_event=domain_event)
