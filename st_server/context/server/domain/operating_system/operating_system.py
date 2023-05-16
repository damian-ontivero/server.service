"""Operating system entity.

This is the aggregate root entity of the Operating system aggregate.
"""

from st_server.shared.core.aggregate_root import AggregateRoot
from st_server.shared.core.domain_event import DomainEvent
from st_server.shared.core.entity_id import EntityId


class OperatingSystem(AggregateRoot):
    """Operating system entity."""

    class NameChanged(DomainEvent):
        """Domain event for name changed."""

        pass

    class VersionChanged(DomainEvent):
        """Domain event for version changed."""

        pass

    class ArchitectChanged(DomainEvent):
        """Domain event for architect changed."""

        pass

    def __init__(
        self,
        id: EntityId | None = None,
        name: str | None = None,
        version: str | None = None,
        architect: str | None = None,
        discarded: bool | None = None,
    ) -> None:
        """Constructor of the operating system entity.

        Important:
            This constructor should not be used directly to generate the entity.
            It should be used only by the repository to instantiate the entity from the database.

            In order to create/generate/register a new operating system, use the `OperatingSystem.create` method.

        Args:
            id (`EntityId`): Operating system id.
            name (`str`): Operating system name.
            version (`str`): Operating system version.
            architect (`str`): Operating system architect.
            discarded (`bool`): Indicates if the operating system is discarded.
        """
        super().__init__(id=id, discarded=discarded)
        self._name = name
        self._version = version
        self._architect = architect

    @property
    def name(self) -> str:
        """Returns the Operating system name.

        Returns:
            `str`: Operating system name.
        """
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Sets the name of the Operating system.

        Args:
            value (`str`): Name of the Operating system.
        """
        if self._name == value:
            return

        domain_event = OperatingSystem.NameChanged(
            type_="operating_system_updated",
            aggregate_id=self.id,
            name=value,
            version=self.version,
            architect=self.architect,
        )
        self._name = value
        self.register_domain_event(domain_event=domain_event)

    @property
    def version(self) -> str:
        """Returns the Operating system name.

        Returns:
            `str`: Operating system name.
        """
        return self._version

    @version.setter
    def version(self, value: str) -> None:
        """Sets the name of the Operating system.

        Args:
            value (`str`): Name of the Operating system.
        """
        if self._version == value:
            return

        domain_event = OperatingSystem.VersionChanged(
            type_="operating_system_updated",
            aggregate_id=self.id,
            name=self.name,
            version=value,
            architect=self.architect,
        )
        self._version = value
        self.register_domain_event(domain_event=domain_event)

    @property
    def architect(self) -> str:
        """Returns the Operating system name.

        Returns:
            `str`: Operating system name.
        """
        return self._architect

    @architect.setter
    def architect(self, value: str) -> None:
        """Sets the name of the Operating system.

        Args:
            value (`str`): Name of the Operating system.
        """
        if self._architect == value:
            return

        domain_event = OperatingSystem.ArchitectChanged(
            type_="operating_system_updated",
            aggregate_id=self.id,
            name=self.name,
            version=self.version,
            architect=value,
        )
        self._architect = value
        self.register_domain_event(domain_event=domain_event)

    def __repr__(self) -> str:
        """Returns the string representation of the object.

        Returns:
            `str`: String representation of the object.
        """
        return (
            "{d}{c}(id={id!r}, name={name!r}, "
            "version={version!r}, architect={architect!r}, "
            "discarded={discarded!r})"
        ).format(
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
            "version": self._version,
            "architect": self._architect,
            "discarded": self._discarded,
        }

    @staticmethod
    def from_dict(data: dict) -> "OperatingSystem":
        """Returns an instance of the class based on the provided dictionary.

        Args:
            data (`dict`): Dictionary representation of the object.

        Returns:
            `OperatingSystem`: Instance of the class.
        """
        return OperatingSystem(**data)

    @staticmethod
    def create(name: str, version: str, architect: str) -> "OperatingSystem":
        """Operating system factory method.

        Important:
            This method is only used to create a new Operating system.
            When creating a new Operating system, the id is automatically generated
            and a domain event is registered.

        Args:
            name (`str`): Operating system name.
            version (`str`): Operating system version.
            architect (`str`): Operating system architect.

        Returns:
            `OperatingSystem`: Operating system instance.
        """
        operating_system = OperatingSystem(
            id=EntityId().value,
            name=name,
            version=version,
            architect=architect,
        )

        domain_event = OperatingSystem.Created(
            type_="operating_system_created", aggregate_id=operating_system.id
        )
        operating_system.register_domain_event(domain_event=domain_event)

        return operating_system

    def discard(self) -> None:
        """Operating system discard method.

        Important:
            This method is only used to discard a Operating system.
            When discarding a Operating system, the discarded attribute is set to True
            and a domain event is registered.
        """
        domain_event = OperatingSystem.Discarded(
            type_="operating_system_discarded", aggregate_id=self._id
        )

        self._discarded = True
        self.register_domain_event(domain_event=domain_event)
