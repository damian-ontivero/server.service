"""Server entity.

This is the aggregate root entity of the server aggregate.
"""

from st_server.server.domain.entity.credential import Credential
from st_server.server.domain.entity.server_application import (
    ServerApplication,
)
from st_server.server.domain.value_object.environment import Environment
from st_server.server.domain.value_object.operating_system import (
    OperatingSystem,
)
from st_server.server.domain.value_object.server_status import ServerStatus
from st_server.shared.domain.entity.aggregate_root import AggregateRoot
from st_server.shared.domain.value_object.domain_event import DomainEvent
from st_server.shared.domain.value_object.entity_id import EntityId


class Server(AggregateRoot):
    """Server entity."""

    class Created(DomainEvent):
        """Domain event that represents the creation of a Server."""

    class Discarded(DomainEvent):
        """Domain event that represents the discarding of a Server."""

    class NameChanged(DomainEvent):
        """Domain event that represents the change of the name of a Server."""

    class CpuChanged(DomainEvent):
        """Domain event that represents the change of the cpu of a Server."""

    class RamChanged(DomainEvent):
        """Domain event that represents the change of the ram of a Server."""

    class HddChanged(DomainEvent):
        """Domain event that represents the change of the hdd of a Server."""

    class EnvironmentChanged(DomainEvent):
        """Domain event that represents the change of the environment of a Server."""

    class OperatingSystemChanged(DomainEvent):
        """Domain event that represents the change of the operating system of a Server."""

    class CredentialChanged(DomainEvent):
        """Domain event that represents the change of the credentials of a Server."""

    class ApplicationChanged(DomainEvent):
        """Domain event that represents the change of the applications of a Server."""

    class StatusChanged(DomainEvent):
        """Domain event that represents the change of the status of a Server."""

    def __init__(
        self,
        id: EntityId | None = None,
        name: str | None = None,
        cpu: str | None = None,
        ram: str | None = None,
        hdd: str | None = None,
        environment: Environment | None = None,
        operating_system: OperatingSystem | None = None,
        credentials: list[Credential] | None = None,
        applications: list[ServerApplication] | None = None,
        status: ServerStatus | None = None,
        discarded: bool | None = None,
    ) -> None:
        """Initialize the Server.

        Important:
            Do not use directly to create a new Server.
            Use the factory method `Server.create` instead.
        """
        super().__init__(id=id, discarded=discarded)
        self._name = name
        self._cpu = cpu
        self._ram = ram
        self._hdd = hdd
        self._environment = environment
        self._operating_system = operating_system
        self._credentials = credentials
        self._applications = applications
        self._status = status

    @property
    def name(self) -> str:
        """Returns the name of the Server."""
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        """Sets the name of the Server."""
        self._check_not_discarded()
        domain_event = Server.NameChanged(
            aggregate_id=self._id.value,
            old_value=self._name,
            new_value=name,
        )
        self._name = name
        self.register_domain_event(domain_event=domain_event)

    @property
    def cpu(self) -> str:
        """Returns the cpu of the Server."""
        return self._cpu

    @cpu.setter
    def cpu(self, cpu: str) -> None:
        """Sets the cpu of the Server."""
        self._check_not_discarded()
        domain_event = Server.CpuChanged(
            aggregate_id=self._id.value,
            old_value=self._cpu,
            new_value=cpu,
        )
        self._cpu = cpu
        self.register_domain_event(domain_event=domain_event)

    @property
    def ram(self) -> str:
        """Returns the ram of the Server."""
        return self._ram

    @ram.setter
    def ram(self, ram: str) -> None:
        """Sets the ram of the Server."""
        self._check_not_discarded()
        domain_event = Server.RamChanged(
            aggregate_id=self._id.value,
            old_value=self._ram,
            new_value=ram,
        )
        self._ram = ram
        self.register_domain_event(domain_event=domain_event)

    @property
    def hdd(self) -> str:
        """Returns the hdd of the Server."""
        return self._hdd

    @hdd.setter
    def hdd(self, hdd: str) -> None:
        """Sets the hdd of the Server."""
        self._check_not_discarded()
        domain_event = Server.HddChanged(
            aggregate_id=self._id.value,
            old_value=self._hdd,
            new_value=hdd,
        )
        self._hdd = hdd
        self.register_domain_event(domain_event=domain_event)

    @property
    def environment(self) -> Environment:
        """Returns the environment of the Server."""
        return self._environment

    @environment.setter
    def environment(self, environment: Environment) -> None:
        """Sets the environment of the Server."""
        self._check_not_discarded()
        domain_event = Server.EnvironmentChanged(
            aggregate_id=self._id.value,
            old_value=self._environment.value,
            new_value=environment.value,
        )
        self._environment = environment
        self.register_domain_event(domain_event=domain_event)

    @property
    def operating_system(self) -> OperatingSystem:
        """Returns the operating system of the Server."""
        return self._operating_system

    @operating_system.setter
    def operating_system(self, operating_system: OperatingSystem) -> None:
        """Sets the operating system of the Server."""
        self._check_not_discarded()
        domain_event = Server.OperatingSystemChanged(
            aggregate_id=self._id.value,
            old_value=self._operating_system.__dict__,
            new_value=operating_system.__dict__,
        )
        self._operating_system = operating_system
        self.register_domain_event(domain_event=domain_event)

    @property
    def credentials(self) -> list[Credential]:
        """Returns the credentials of the Server."""
        return self._credentials

    @credentials.setter
    def credentials(self, credentials: list[Credential]) -> None:
        """Sets the credentials of the Server."""
        self._check_not_discarded()
        domain_event = Server.CredentialChanged(
            aggregate_id=self._id.value,
            old_value=[
                credential.to_dict() for credential in self._credentials
            ],
            new_value=[credential.to_dict() for credential in credentials],
        )
        self._credentials = credentials
        self.register_domain_event(domain_event=domain_event)

    @property
    def applications(self) -> list[ServerApplication]:
        """Returns the applications of the Server."""
        return self._applications

    @applications.setter
    def applications(self, applications: list[ServerApplication]) -> None:
        """Sets the applications of the Server."""
        self._check_not_discarded()
        domain_event = Server.ApplicationChanged(
            aggregate_id=self._id.value,
            old_value=self._applications,
            new_value=applications,
        )
        self._applications = applications
        self.register_domain_event(domain_event=domain_event)

    @property
    def status(self) -> ServerStatus:
        """Returns the status of the Server."""
        return self._status

    @status.setter
    def status(self, status: ServerStatus) -> None:
        """Sets the status of the Server."""
        self._check_not_discarded()
        domain_event = Server.StatusChanged(
            aggregate_id=self._id.value,
            old_value=self._status.value,
            new_value=status.value,
        )
        self._status = status
        self.register_domain_event(domain_event=domain_event)

    def __repr__(self) -> str:
        """Returns the string representation of the Server."""
        return (
            "{d}{c}(id={id!r}, name={name!r}, "
            "cpu={cpu!r}, ram={ram!r}, hdd={hdd!r}, "
            "environment={environment!r}, "
            "operating_system={operating_system!r}, "
            "credentials={credentials!r}, "
            "applications={applications!r}, "
            "status={status!r}, "
            "discarded={discarded!r})"
        ).format(
            d="*Discarded*" if self._discarded else "",
            c=self.__class__.__name__,
            id=self._id,
            name=self._name,
            cpu=self._cpu,
            ram=self._ram,
            hdd=self._hdd,
            environment=self._environment,
            operating_system=self._operating_system,
            credentials=self._credentials,
            applications=self._applications,
            status=self._status,
            discarded=self._discarded,
        )

    def to_dict(self) -> dict:
        """Returns the dictionary representation of the Server."""
        return {
            "id": self._id.value,
            "name": self._name,
            "cpu": self._cpu,
            "ram": self._ram,
            "hdd": self._hdd,
            "environment": self._environment.value
            if self._environment
            else None,
            "operating_system": self._operating_system.__dict__
            if self._operating_system
            else None,
            "credentials": [
                credential.to_dict() for credential in self._credentials
            ],
            "applications": [
                application.to_dict() for application in self._applications
            ],
            "status": self._status.value if self._status else None,
            "discarded": self._discarded,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Server":
        """Named constructor for creating a Server from a dictionary."""
        return cls(
            id=EntityId.from_text(value=data.get("id")),
            name=data.get("name"),
            cpu=data.get("cpu"),
            ram=data.get("ram"),
            hdd=data.get("hdd"),
            environment=Environment.from_text(value=data.get("environment"))
            if data.get("environment")
            else None,
            operating_system=OperatingSystem.from_dict(
                value=data.get("operating_system")
            )
            if data.get("operating_system")
            else None,
            credentials=[
                Credential.from_dict(data=credential)
                for credential in data.get("credentials")
            ],
            applications=data.get("applications"),
            status=ServerStatus.from_text(value=data.get("status"))
            if data.get("status")
            else None,
            discarded=data.get("discarded"),
        )

    @classmethod
    def create(
        cls,
        name: str,
        cpu: str | None = None,
        ram: str | None = None,
        hdd: str | None = None,
        environment: Environment | None = None,
        operating_system: OperatingSystem | None = None,
        credentials: list[Credential] | None = None,
        applications: list[ServerApplication] | None = None,
    ) -> "Server":
        """Named constructor for creating a new Server.

        Important:
            This method is only used to create a new Server.
            When creating a new Server, the id is automatically generated
            and a domain event is registered.
        """
        server = cls(
            id=EntityId.generate(),
            name=name,
            cpu=cpu,
            ram=ram,
            hdd=hdd,
            environment=environment,
            operating_system=operating_system,
            credentials=credentials or [],
            applications=applications or [],
            status=ServerStatus.from_text(value="stopped"),
            discarded=False,
        )
        domain_event = Server.Created(aggregate_id=server.id.value)
        server.register_domain_event(domain_event=domain_event)
        return server

    def update(
        self,
        name: str | None = None,
        cpu: str | None = ...,
        ram: str | None = ...,
        hdd: str | None = ...,
        environment: Environment | None = None,
        operating_system: OperatingSystem | None = None,
        credentials: list[Credential] | None = None,
        applications: list[ServerApplication] | None = None,
        status: ServerStatus | None = None,
    ) -> "Server":
        """Updates the Server.

        Important:
            This method is only used to update a Server.
            When updating the attributes, the domain events
            are registered by setters.
        """
        if not name == self._name:
            self.name = name
        if cpu is not ... and not cpu == self._cpu:
            self.cpu = cpu
        if ram is not ... and not ram == self._ram:
            self.ram = ram
        if ram is not ... and not hdd == self._hdd:
            self.hdd = hdd
        if not environment == self._environment:
            self.environment = environment
        if not operating_system == self._operating_system:
            self.operating_system = operating_system
        if credentials is not None:
            for current_credential in self._credentials:
                if current_credential not in credentials:
                    self._credentials.remove(current_credential)
            for new_credential in credentials:
                if new_credential not in self._credentials:
                    if not any(
                        [
                            new_credential.connection_type
                            == credential.connection_type
                            and new_credential.username == credential.username
                            for credential in self._credentials
                        ]
                    ):
                        self._credentials.append(
                            Credential.create(
                                server_id=self._id,
                                connection_type=new_credential.connection_type,
                                username=new_credential.username,
                                password=new_credential.password,
                                local_ip=new_credential.local_ip,
                                local_port=new_credential.local_port,
                                public_ip=new_credential.public_ip,
                                public_port=new_credential.public_port,
                            )
                        )

                else:
                    self._credentials[
                        self._credentials.index(new_credential)
                    ].update(
                        server_id=new_credential.server_id,
                        connection_type=new_credential.connection_type,
                        username=new_credential.username,
                        password=new_credential.password,
                        local_ip=new_credential.local_ip,
                        local_port=new_credential.local_port,
                        public_ip=new_credential.public_ip,
                        public_port=new_credential.public_port,
                    )

        if applications is not None:
            self.applications = applications
        if not status == self._status:
            self.status = status
        return self

    def discard(self) -> None:
        """Discards the Server.

        Important:
            This method is only used to discard a Server.
            When discarding a Server, the discarded attribute is set to True
            and a domain event is registered.
        """
        domain_event = Server.Discarded(aggregate_id=self._id.value)
        self._discarded = True
        self.register_domain_event(domain_event=domain_event)
