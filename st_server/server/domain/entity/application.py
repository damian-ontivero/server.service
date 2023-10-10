"""Application entity.

This is the aggregate root entity of the application aggregate.
"""

from st_server.shared.domain.entity.aggregate_root import AggregateRoot
from st_server.shared.domain.value_object.domain_event import DomainEvent
from st_server.shared.domain.value_object.entity_id import EntityId


class Application(AggregateRoot):
    """Application entity."""

    class Created(DomainEvent):
        """Domain event that represents the creation of an Application."""

    class Discarded(DomainEvent):
        """Domain event that represents the discarding of an Application."""

    class NameChanged(DomainEvent):
        """Domain event that represents the change of the name of an Application."""

    class VersionChanged(DomainEvent):
        """Domain event that represents the change of the version of an Application."""

    class ArchitectChanged(DomainEvent):
        """Domain event that represents the change of the architect of an Application."""

    def __init__(
        self,
        id: EntityId | None = None,
        name: str | None = None,
        version: str | None = None,
        architect: str | None = None,
        discarded: bool | None = None,
    ) -> None:
        """Initialize the Application.

        Important:
            Do not use directly to create a new Application.
            Use the factory method `Application.create` instead.
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
        self.register_domain_event(domain_event=domain_event)

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
        self.register_domain_event(domain_event=domain_event)

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
        self.register_domain_event(domain_event=domain_event)

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

    def to_dict(self) -> dict:
        """Returns the dictionary representation of the Application."""
        return {
            "id": self._id.value,
            "name": self._name,
            "version": self._version,
            "architect": self._architect,
            "discarded": self._discarded,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Application":
        """Named constructor for creating an Application from a dictionary."""
        return cls(
            id=EntityId.from_text(data.get("id")),
            name=data.get("name"),
            version=data.get("version"),
            architect=data.get("architect"),
            discarded=data.get("discarded"),
        )

    @classmethod
    def create(cls, name: str, version: str, architect: str) -> "Application":
        """Named constructor for creating a new Application.

        Important:
            This method is only used to create a new Application.
            When creating a new Application, the id is automatically generated
            and a domain event is registered.
        """
        application = cls(
            id=EntityId.generate(),
            name=name,
            version=version,
            architect=architect,
            discarded=False,
        )
        domain_event = Application.Created(aggregate_id=application._id.value)
        application.register_domain_event(domain_event=domain_event)
        return application

    def update(
        self,
        name: str | None = None,
        version: str | None = None,
        architect: str | None = None,
    ) -> None:
        """Updates the Application.

        Important:
            This method is only used to update an Application.
            When updating the attributes, the domain events
            are registered by setters.
        """
        if name and not name == self._name:
            self.name = name
        if version and not version == self._version:
            self.version = version
        if architect and not architect == self._architect:
            self.architect = architect
        return self

    def discard(self) -> None:
        """Discards the Application.

        Important:
            This method is only used to discard an Application.
            When discarding an Application, the discarded attribute is set to True
            and a domain event is registered.
        """
        domain_event = Application.Discarded(aggregate_id=self._id.value)
        self._discarded = True
        self.register_domain_event(domain_event=domain_event)
