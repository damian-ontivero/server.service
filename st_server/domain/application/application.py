"""Application entity.

This is the aggregate root entity of the application aggregate.
"""

from st_server.domain.aggregate_root import AggregateRoot
from st_server.domain.domain_event import DomainEvent
from st_server.domain.entity_id import EntityId


class Application(AggregateRoot):
    """Application entity."""

    class NameChanged(DomainEvent):
        """Domain event for name changed."""

        pass

    class VersionChanged(DomainEvent):
        """Domain event for version changed."""

        pass

    class ArchitectChanged(DomainEvent):
        """Domain event for email changed."""

        pass

    def __init__(
        self,
        id: EntityId | None = None,
        name: str | None = None,
        version: str | None = None,
        architect: str | None = None,
        discarded: bool | None = None,
    ) -> None:
        """Constructor of the application entity.

        Important:
            This constructor should not be used directly to generate the entity.
            It should be used only by the repository to instantiate the entity from the database.

            In order to create/generate/register a new application, use the `Application.create` method.

        Args:
            id (`EntityId`): Application id.
            name (`str`): Application name.
            version (`str`): Application version.
            architect (`str`): Application architect.
            discarded (`bool`): Indicates if the application is discarded.
        """
        super().__init__(id=id, discarded=discarded)
        self._name = name
        self._version = version
        self._architect = architect

    @property
    def name(self) -> str:
        """Returns the name of the application.

        Returns:
            `str`: Name of the application.
        """
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Sets the name of the application.

        Args:
            value (`str`): Name of the application.
        """
        if self._name == value:
            return

        domain_event = Application.NameChanged(
            type_="application_updated",
            aggregate_id=self.id,
            old_value=self._name,
            new_value=value,
        )

        self._name = value
        self.register_domain_event(domain_event=domain_event)

    @property
    def version(self) -> str:
        """Returns the version of the application.

        Returns:
            `str`: Version of the application.
        """
        return self._version

    @version.setter
    def version(self, value: str) -> None:
        """Sets the version of the application.

        Args:
            value (`str`): Version of the application.
        """
        if self._version == value:
            return

        domain_event = Application.VersionChanged(
            type_="application_updated",
            aggregate_id=self.id,
            old_value=self._version,
            new_value=value,
        )

        self._version = value
        self.register_domain_event(domain_event=domain_event)

    @property
    def architect(self) -> str:
        """Returns the architect of the application.

        Returns:
            `str`: Architect of the application.
        """
        return self._architect

    @architect.setter
    def architect(self, value: str) -> None:
        """Sets the architect of the application.

        Args:
            value (`str`): Architect of the application.
        """
        if self._architect == value:
            return

        domain_event = Application.ArchitectChanged(
            type_="application_updated",
            aggregate_id=self.id,
            old_value=self._architect,
            new_value=value,
        )

        self._architect = value
        self.register_domain_event(domain_event=domain_event)

    def __repr__(self) -> str:
        """Returns the string representation of the object.

        Returns:
            `str`: String representation of the object.
        """
        return f"{self.__class__.__name__}(id={self.id}, name={self._name}, version={self._version}, architect={self._architect}, discarded={self._discarded})"

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
    def from_dict(data: dict) -> "Application":
        """Returns an instance of the class based on the provided dictionary.

        Args:
            data (`dict`): Dictionary representation of the object.

        Returns:
            `Application`: Instance of the class.
        """
        return Application(**data)

    @staticmethod
    def create(name: str, version: str, architect: str) -> "Application":
        """Application factory method.

        Important:
            This method is only used to create a new application.
            When creating a new application, the id is automatically generated
            and a domain event is registered.

        Args:
            name (`str`): Application name.
            version (`str`): Application version.
            architect (`str`): Application architect.

        Returns:
            `Application`: Application instance.
        """
        application = Application(
            id=EntityId().value,
            name=name,
            version=version,
            architect=architect,
        )

        domain_event = Application.Created(
            type_="application_created", aggregate_id=application.id
        )
        application.register_domain_event(domain_event=domain_event)

        return application

    def discard(self) -> None:
        """Application discard method.

        Important:
            This method is only used to discard an application.
            When discarding an application, the discarded attribute is set to True
            and a domain event is registered.
        """
        domain_event = Application.Discarded(
            type_="application_discarded", aggregate_id=self._id
        )

        self._discarded = True
        self.register_domain_event(domain_event=domain_event)
