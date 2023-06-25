"""Server entity.

This is the aggregate root entity of the server aggregate.
"""

from st_server.context.server.domain.entity.credential import Credential
from st_server.context.server.domain.entity.environment import Environment
from st_server.context.server.domain.entity.operating_system import (
    OperatingSystem,
)
from st_server.context.server.domain.entity.server_application import (
    ServerApplication,
)
from st_server.context.server.domain.value_object.server_status import (
    ServerStatus,
)
from st_server.shared.core.aggregate_root import AggregateRoot
from st_server.shared.core.domain_event import DomainEvent
from st_server.shared.core.entity_id import EntityId


class Server(AggregateRoot):
    """Server entity."""

    class Created(DomainEvent):
        pass

    class Discarded(DomainEvent):
        pass

    class NameChanged(DomainEvent):
        pass

    class CpuChanged(DomainEvent):
        pass

    class RamChanged(DomainEvent):
        pass

    class HddChanged(DomainEvent):
        pass

    class EnvironmentChanged(DomainEvent):
        pass

    class OperatingSystemChanged(DomainEvent):
        pass

    class CredentialChanged(DomainEvent):
        pass

    class ApplicationChanged(DomainEvent):
        pass

    class StatusChanged(DomainEvent):
        pass

    def __init__(
        self,
        id: EntityId | None = None,
        name: str | None = None,
        cpu: str | None = None,
        ram: str | None = None,
        hdd: str | None = None,
        environment_id: EntityId | None = None,
        environment: Environment | None = None,
        operating_system_id: EntityId | None = None,
        operating_system: OperatingSystem | None = None,
        credentials: list[Credential] | None = None,
        applications: list[ServerApplication] | None = None,
        status: ServerStatus | None = None,
        discarded: bool | None = None,
    ) -> None:
        """
        Important:
            Do not use directly to create a new Server.
            Use the factory method `Server.create` instead.
        """
        super().__init__(id=id, discarded=discarded)
        self._name = name
        self._cpu = cpu
        self._ram = ram
        self._hdd = hdd
        self._environment_id = environment_id
        self._environment = environment
        self._operating_system_id = operating_system_id
        self._operating_system = operating_system
        self._credentials = credentials
        self._status = status
        self._applications = applications

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._check_not_discarded()
        domain_event = Server.NameChanged(
            aggregate_id=self.id.value,
            old_value=self.name,
            new_value=value,
        )
        self._name = value
        self.register_domain_event(domain_event=domain_event)

    @property
    def cpu(self) -> str:
        return self._cpu

    @cpu.setter
    def cpu(self, value: str) -> None:
        self._check_not_discarded()
        domain_event = Server.CpuChanged(
            aggregate_id=self.id.value,
            old_value=self.cpu,
            new_value=value,
        )
        self._cpu = value
        self.register_domain_event(domain_event=domain_event)

    @property
    def ram(self) -> str:
        return self._ram

    @ram.setter
    def ram(self, value: str) -> None:
        self._check_not_discarded()
        domain_event = Server.RamChanged(
            aggregate_id=self.id.value,
            old_value=self.ram,
            new_value=value,
        )
        self._ram = value
        self.register_domain_event(domain_event=domain_event)

    @property
    def hdd(self) -> str:
        return self._hdd

    @hdd.setter
    def hdd(self, value: str) -> None:
        self._check_not_discarded()
        domain_event = Server.HddChanged(
            aggregate_id=self.id.value,
            old_value=self.hdd,
            new_value=value,
        )
        self._hdd = value
        self.register_domain_event(domain_event=domain_event)

    @property
    def environment_id(self) -> EntityId:
        return self._environment_id

    @environment_id.setter
    def environment_id(self, value: EntityId) -> None:
        self._check_not_discarded()
        domain_event = Server.EnvironmentChanged(
            aggregate_id=self.id.value,
            old_value=self.environment_id.__dict__,
            new_value=value.__dict__,
        )
        self._environment_id = value
        self.register_domain_event(domain_event=domain_event)

    @property
    def environment(self) -> Environment:
        return self._environment

    @property
    def operating_system_id(self) -> EntityId:
        return self._operating_system_id

    @operating_system_id.setter
    def operating_system_id(self, value: EntityId) -> None:
        self._check_not_discarded()
        domain_event = Server.OperatingSystemChanged(
            aggregate_id=self.id.value,
            old_value=self.operating_system_id.__dict__,
            new_value=value.__dict__,
        )
        self._operating_system_id = value
        self.register_domain_event(domain_event=domain_event)

    @property
    def operating_system(self) -> OperatingSystem:
        return self._operating_system

    @property
    def credentials(self) -> list[Credential]:
        return self._credentials

    @credentials.setter
    def credentials(self, value: list[Credential]) -> None:
        self._check_not_discarded()
        domain_event = Server.CredentialChanged(
            aggregate_id=self.id.value,
            old_value=self.credentials,
            new_value=value,
        )
        self._credentials = value
        self.register_domain_event(domain_event=domain_event)

    @property
    def applications(self) -> list[ServerApplication]:
        return self._applications

    @applications.setter
    def applications(self, value: list[ServerApplication]) -> None:
        self._check_not_discarded()
        domain_event = Server.ApplicationChanged(
            aggregate_id=self.id.value,
            old_value=self.applications,
            new_value=value,
        )
        self._applications = value
        self.register_domain_event(domain_event=domain_event)

    @property
    def status(self) -> ServerStatus:
        return self._status

    @status.setter
    def status(self, value: ServerStatus) -> None:
        self._check_not_discarded()
        domain_event = Server.StatusChanged(
            aggregate_id=self.id.value,
            old_value=self.status,
            new_value=value,
        )
        self._status = value
        self.register_domain_event(domain_event=domain_event)

    def __repr__(self) -> str:
        return (
            "{d}{c}(id={id!r}, name={name!r}, "
            "cpu={cpu!r}, ram={ram!r}, hdd={hdd!r}, "
            "environment_id={environment_id!r}, "
            "environment={environment!r}, "
            "operating_system_id={operating_system_id!r}, "
            "operating_system={operating_system!r}, "
            "credentials={credentials!r}, "
            "applications={applications!r}, "
            "status={status!r}, "
            "discarded={discarded!r})"
        ).format(
            d="*Discarded*" if self.discarded else "",
            c=self.__class__.__name__,
            id=self.id,
            name=self.name,
            cpu=self.cpu,
            ram=self.ram,
            hdd=self.hdd,
            environment_id=self.environment_id,
            environment=self.environment,
            operating_system_id=self.operating_system_id,
            operating_system=self.operating_system,
            credentials=self.credentials,
            applications=self.applications,
            status=self.status,
            discarded=self.discarded,
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id.value,
            "name": self.name,
            "cpu": self.cpu,
            "ram": self.ram,
            "hdd": self.hdd,
            "environment_id": self.environment_id.value,
            "environment": self.environment.to_dict()
            if self.environment
            else None,
            "operating_system_id": self.operating_system_id.value,
            "operating_system": self.operating_system.to_dict()
            if self.operating_system
            else None,
            "credentials": [
                credential.to_dict() for credential in self.credentials
            ],
            "applications": [
                application.to_dict() for application in self.applications
            ],
            "status": self.status.value if self.status else None,
            "discarded": self.discarded,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Server":
        return cls(
            id=EntityId.from_string(value=data.get("id")),
            name=data.get("name"),
            cpu=data.get("cpu"),
            ram=data.get("ram"),
            hdd=data.get("hdd"),
            environment_id=EntityId.from_string(
                value=data.get("environment_id")
            ),
            environment=Environment.from_dict(data=data.get("environment"))
            if data.get("environment")
            else None,
            operating_system_id=EntityId.from_string(
                value=data.get("operating_system_id")
            ),
            operating_system=OperatingSystem.from_dict(
                data=data.get("operating_system")
            )
            if data.get("operating_system")
            else None,
            credentials=data.get("credentials"),
            applications=data.get("applications"),
            status=ServerStatus.from_string(value=data.get("status"))
            if data.get("status")
            else None,
            discarded=data.get("discarded"),
        )

    @classmethod
    def create(
        cls,
        name: str,
        cpu: str,
        ram: str,
        hdd: str,
        environment_id: EntityId,
        operating_system_id: EntityId,
        credentials: list[Credential] | None = None,
        applications: list[ServerApplication] | None = None,
    ) -> "Server":
        """
        Important:
            This method is only used to create a new server.
            When creating a new server, the id is automatically generated
            and a domain event is registered.
        """
        server = cls(
            id=EntityId.generate(),
            name=name,
            cpu=cpu,
            ram=ram,
            hdd=hdd,
            environment_id=EntityId.from_string(value=environment_id),
            operating_system_id=EntityId.from_string(
                value=operating_system_id
            ),
            credentials=credentials or [],
            applications=applications or [],
        )
        domain_event = Server.Created(aggregate_id=server.id.value)
        server.register_domain_event(domain_event=domain_event)
        return server

    def update(
        self,
        name: str | None = None,
        cpu: str | None = None,
        ram: str | None = None,
        hdd: str | None = None,
        environment_id: EntityId | None = None,
        operating_system_id: EntityId | None = None,
        credentials: list[Credential] | None = None,
        applications: list[ServerApplication] | None = None,
        status: ServerStatus | None = None,
    ) -> "Server":
        """
        Important:
            This method is only used to update a server.
            When updating the attributes, the domain events
            are registered by setters.
        """
        if not self.name == name:
            self.name = name
        if not self.cpu == cpu:
            self.cpu = cpu
        if not self.ram == ram:
            self.ram = ram
        if not self.hdd == hdd:
            self.hdd = hdd
        if not self.environment_id == environment_id:
            self.environment_id = environment_id
        if not self.operating_system_id == operating_system_id:
            self.operating_system_id = operating_system_id
        if not self.credentials == credentials:
            self.credentials = credentials
        if not self.applications == applications:
            self.applications = applications
        if not self.status == status:
            self.status = status
        return self

    def discard(self) -> None:
        """
        Important:
            This method is only used to discard a server.
            When discarding a server, the discarded attribute is set to True
            and a domain event is registered.
        """
        domain_event = Server.Discarded(aggregate_id=self.id.value)
        self.discarded = True
        self.register_domain_event(domain_event=domain_event)
