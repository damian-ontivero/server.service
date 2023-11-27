"""Application entity.

This is the aggregate root entity of the Application aggregate.
"""

from st_core.domain.aggregate_root import AggregateRoot
from st_core.domain.domain_event import DomainEvent
from st_core.domain.entity_id import EntityId


class Application(AggregateRoot):
    """Application entity."""

    class Created(DomainEvent):
        """Domain event that represents the creation of an Application."""

        pass

    class NameChanged(DomainEvent):
        """Domain event that represents the change of the name of an Application."""

        pass

    class VersionChanged(DomainEvent):
        """Domain event that represents the change of the version of an Application."""

        pass

    class ArchitectChanged(DomainEvent):
        """Domain event that represents the change of the architect of an Application."""

        pass

    def __init__(
        self,
        id: EntityId | None = None,
        name: str | None = None,
        version: str | None = None,
        architect: str | None = None,
        discarded: bool | None = None,
    ) -> None:
        """Initializes the Application.

        Important:
            Do not use directly to create a new Application.
            Use the Application Factory instead.
        """
        super().__init__(id=id, discarded=discarded)
        self._name = name
        self._version = version
        self._architect = architect

    @property
    def name(self) -> str:
        """Returns the name of the Application."""
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        """Sets the name of the Application."""
        self._check_not_discarded()
        domain_event = Application.NameChanged(
            aggregate_id=self._id.value,
            old_value=self._name,
            new_value=name,
        )
        self._name = name
        self.register_domain_event(domain_event)

    @property
    def version(self) -> str:
        """Returns the version of the Application."""
        return self._version

    @version.setter
    def version(self, version: str) -> None:
        """Sets the version of the Application."""
        self._check_not_discarded()
        domain_event = Application.VersionChanged(
            aggregate_id=self._id.value,
            old_value=self._version,
            new_value=version,
        )
        self._version = version
        self.register_domain_event(domain_event)

    @property
    def architect(self) -> str:
        """Returns the architect of the Application."""
        return self._architect

    @architect.setter
    def architect(self, architect: str) -> None:
        """Sets the architect of the Application."""
        self._check_not_discarded()
        domain_event = Application.ArchitectChanged(
            aggregate_id=self._id.value,
            old_value=self._architect,
            new_value=architect,
        )
        self._architect = architect
        self.register_domain_event(domain_event)

    def update(self, name: str, version: str, architect: str) -> None:
        """Updates the Application.

        Important:
            This method is only used to update an existing Application.
        """
        self.name = name
        self.version = version
        self.architect = architect

    def __repr__(self) -> str:
        """Returns the string representation of the Application."""
        return (
            "{d}{c}(id={id!r}, name={name!r}, "
            "version={version!r}, architect={architect!r}, "
            "discarded={discarded!r})"
        ).format(
            d="*Discarded*" if self._discarded else "",
            c=self.__class__.__name__,
            id=self._id.value,
            name=self._name,
            version=self._version,
            architect=self._architect,
            discarded=self._discarded,
        )
