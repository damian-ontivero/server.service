from st_server.shared.domain.aggregate_root import AggregateRoot
from st_server.shared.domain.domain_event import DomainEvent
from st_server.shared.domain.entity_id import EntityId


class Application(AggregateRoot):
    class Registered(DomainEvent):
        pass

    def __init__(
        self,
        id: EntityId,
        name: str,
        version: str,
        architect: str,
        discarded: bool,
    ) -> None:
        """
        Important:
            Do not use directly to create a new Application.
            Use the Application Factory instead.
        """
        super().__init__(id=id, discarded=discarded)
        self._name = name
        self._version = version
        self._architect = architect

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

    @property
    def name(self) -> str:
        self._check_not_discarded()
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._check_not_discarded()
        self._name = name
        self._register_domain_event(
            Application.Modified(
                aggregate_id=self._id.value,
                old_value=self._name,
                new_value=name,
            )
        )

    @property
    def version(self) -> str:
        self._check_not_discarded()
        return self._version

    @version.setter
    def version(self, version: str) -> None:
        self._check_not_discarded()
        self._version = version
        self._register_domain_event(
            Application.Modified(
                aggregate_id=self._id.value,
                old_value=self._version,
                new_value=version,
            )
        )

    @property
    def architect(self) -> str:
        self._check_not_discarded()
        return self._architect

    @architect.setter
    def architect(self, architect: str) -> None:
        self._check_not_discarded()
        self._architect = architect
        self._register_domain_event(
            Application.Modified(
                aggregate_id=self._id.value,
                old_value=self._architect,
                new_value=architect,
            )
        )

    @staticmethod
    def register(name: str, version: str, architect: str) -> "Application":
        """Named constructor to register a new entity."""
        application = Application(
            id=EntityId.generate(),
            name=name,
            version=version,
            architect=architect,
            discarded=False,
        )
        application._register_domain_event(
            Application.Registered(aggregate_id=application.id.value)
        )
        return application

    @staticmethod
    def from_primitive_values(
        id: str, name: str, version: str, architect: str, discarded: bool
    ) -> "Application":
        """Named constructor to restore the entity from its primitive values."""
        return Application(
            id=EntityId.from_text(id),
            name=name,
            version=version,
            architect=architect,
            discarded=discarded,
        )

    def discard(self) -> None:
        """Discards the entity."""
        self._check_not_discarded()
        self._discarded = True
        self._register_domain_event(
            Application.Discarded(aggregate_id=self._id.value)
        )