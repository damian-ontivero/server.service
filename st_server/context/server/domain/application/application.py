"""Application entity.

This is the aggregate root entity of the application aggregate.
"""

from st_server.shared.core.aggregate_root import AggregateRoot
from st_server.shared.core.domain_event import DomainEvent
from st_server.shared.core.entity_id import EntityId


class Application(AggregateRoot):
    """Application entity."""

    class Created(DomainEvent):
        pass

    class Discarded(DomainEvent):
        pass

    class NameChanged(DomainEvent):
        pass

    class VersionChanged(DomainEvent):
        pass

    class ArchitectChanged(DomainEvent):
        pass

    def __init__(
        self,
        id: EntityId | None = None,
        name: str | None = None,
        version: str | None = None,
        architect: str | None = None,
        discarded: bool | None = None,
    ) -> None:
        """
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
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._check_not_discarded()
        domain_event = Application.NameChanged(
            aggregate_id=self._id.value,
            old_value=self._name,
            new_value=value,
        )
        self._name = value
        self.register_domain_event(domain_event=domain_event)

    @property
    def version(self) -> str:
        return self._version

    @version.setter
    def version(self, value: str) -> None:
        self._check_not_discarded()
        domain_event = Application.VersionChanged(
            aggregate_id=self._id.value,
            old_value=self._version,
            new_value=value,
        )
        self._version = value
        self.register_domain_event(domain_event=domain_event)

    @property
    def architect(self) -> str:
        return self._architect

    @architect.setter
    def architect(self, value: str) -> None:
        self._check_not_discarded()
        domain_event = Application.ArchitectChanged(
            aggregate_id=self._id.value,
            old_value=self._architect,
            new_value=value,
        )
        self._architect = value
        self.register_domain_event(domain_event=domain_event)

    def __repr__(self) -> str:
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
        return {
            "id": self._id.value,
            "name": self._name,
            "version": self._version,
            "architect": self._architect,
            "discarded": self._discarded,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Application":
        return cls(
            id=EntityId.from_string(data.get("id")),
            name=data.get("name"),
            version=data.get("version"),
            architect=data.get("architect"),
            discarded=data.get("discarded"),
        )

    @classmethod
    def create(cls, name: str, version: str, architect: str) -> "Application":
        """
        Important:
            This method is only used to create a new application.
            When creating a new application, the id is automatically generated
            and a domain event is registered.
        """
        application = cls(
            id=EntityId.generate(),
            name=name,
            version=version,
            architect=architect,
        )
        domain_event = Application.Created(aggregate_id=application.id)
        application.register_domain_event(domain_event=domain_event)
        return application

    def update(
        self,
        name: str | None = None,
        version: str | None = None,
        architect: str | None = None,
    ) -> None:
        """
        Important:
            This method is only used to update an application.
            When updating the attributes, the domain events
            are registered by setters.
        """
        if not self.name == name:
            self.name = name
        if not self.version == version:
            self.version = version
        if not self.architect == architect:
            self.architect = architect
        return self

    def discard(self) -> None:
        """
        Important:
            This method is only used to discard an application.
            When discarding an application, the discarded attribute is set to True
            and a domain event is registered.
        """
        domain_event = Application.Discarded(aggregate_id=self._id)
        self._discarded = True
        self.register_domain_event(domain_event=domain_event)
