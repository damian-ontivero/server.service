"""Server entity.

This is the aggregate root entity of the server aggregate.
"""

from st_server.server.domain.entities.credential import Credential
from st_server.server.domain.entities.server_application import (
    ServerApplication,
)
from st_server.server.domain.value_objects.environment import Environment
from st_server.server.domain.value_objects.operating_system import (
    OperatingSystem,
)
from st_server.server.domain.value_objects.server_status import ServerStatus
from st_server.shared.domain.entities.aggregate_root import AggregateRoot
from st_server.shared.domain.value_objects.domain_event import DomainEvent
from st_server.shared.domain.value_objects.entity_id import EntityId


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
        environment: Environment | None = None,
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
        self._environment = environment
        self._operating_system = operating_system
        self._credentials = credentials
        self._applications = applications
        self._status = status

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
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
        return self._cpu

    @cpu.setter
    def cpu(self, cpu: str) -> None:
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
        return self._ram

    @ram.setter
    def ram(self, ram: str) -> None:
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
        return self._hdd

    @hdd.setter
    def hdd(self, hdd: str) -> None:
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
        return self._environment

    @environment.setter
    def environment(self, environment: Environment) -> None:
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
        return self._operating_system

    @operating_system.setter
    def operating_system(self, operating_system: OperatingSystem) -> None:
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
        return self._credentials

    @credentials.setter
    def credentials(self, credentials: list[Credential]) -> None:
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
        return self._applications

    @applications.setter
    def applications(self, applications: list[ServerApplication]) -> None:
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
        return self._status

    @status.setter
    def status(self, status: ServerStatus) -> None:
        self._check_not_discarded()
        domain_event = Server.StatusChanged(
            aggregate_id=self._id.value,
            old_value=self._status.value,
            new_value=status.value,
        )
        self._status = status
        self.register_domain_event(domain_event=domain_event)

    def __repr__(self) -> str:
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
            id=self._id.value,
            name=self._name,
            cpu=self._cpu,
            ram=self._ram,
            hdd=self._hdd,
            environment=self._environment.value,
            operating_system=self._operating_system.__dict__,
            credentials=self._credentials,
            applications=self._applications,
            status=self._status.value,
            discarded=self._discarded,
        )

    def to_dict(self) -> dict:
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
        return cls(
            id=EntityId.from_string(value=data.get("id")),
            name=data.get("name"),
            cpu=data.get("cpu"),
            ram=data.get("ram"),
            hdd=data.get("hdd"),
            environment=Environment.from_string(value=data.get("environment"))
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
        environment: Environment | None = None,
        operating_system: OperatingSystem | None = None,
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
            environment=environment,
            operating_system=operating_system,
            credentials=credentials or [],
            applications=applications or [],
            status=ServerStatus.from_string(value="stopped"),
            discarded=False,
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
        environment: Environment | None = None,
        operating_system: OperatingSystem | None = None,
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
        if name is not None and not name == self._name:
            self.name = name
        if cpu is not None and not cpu == self._cpu:
            self.cpu = cpu
        if ram is not None and not ram == self._ram:
            self.ram = ram
        if hdd is not None and not hdd == self._hdd:
            self.hdd = hdd
        if environment is not None and not environment == self._environment:
            self.environment = environment
        if (
            operating_system is not None
            and not operating_system == self._operating_system
        ):
            self.operating_system = operating_system

        if credentials is not None:
            # If the new list of credentials does not contain the current credential, remove it.
            # If the current list of credentials does not contain the new credential, add it.
            # If the current list of credentials contains the new credential, update it.
            for current_credential in self._credentials:
                if current_credential not in credentials:
                    self._credentials.remove(current_credential)
            for new_credential in credentials:
                if new_credential not in self._credentials:
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
                    ] = new_credential

        if applications is not None and not applications == self._applications:
            self.applications = applications
        if status is not None and not status == self._status:
            self.status = status
        return self

    def discard(self) -> None:
        """
        Important:
            This method is only used to discard a server.
            When discarding a server, the discarded attribute is set to True
            and a domain event is registered.
        """
        domain_event = Server.Discarded(aggregate_id=self._id.value)
        self._discarded = True
        self.register_domain_event(domain_event=domain_event)
