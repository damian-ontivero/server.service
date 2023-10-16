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
from st_server.server.domain.value_object.connection_type import (
    ConnectionType,
)


class Server(AggregateRoot):
    """Server entity."""

    class NameChanged(DomainEvent):
        """Domain event that represents the change of the name of a Server."""

        pass

    class CpuChanged(DomainEvent):
        """Domain event that represents the change of the cpu of a Server."""

        pass

    class RamChanged(DomainEvent):
        """Domain event that represents the change of the ram of a Server."""

        pass

    class HddChanged(DomainEvent):
        """Domain event that represents the change of the hdd of a Server."""

        pass

    class EnvironmentChanged(DomainEvent):
        """Domain event that represents the change of the environment of a Server."""

        pass

    class OperatingSystemChanged(DomainEvent):
        """Domain event that represents the change of the operating system of a Server."""

        pass

    class CredentialChanged(DomainEvent):
        """Domain event that represents the change of the credentials of a Server."""

        pass

    class ApplicationChanged(DomainEvent):
        """Domain event that represents the change of the applications of a Server."""

        pass

    class StatusChanged(DomainEvent):
        """Domain event that represents the change of the status of a Server."""

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
        """Initializes the Server.

        Important:
            Do not use directly to create a new Server.
            Use the named constructor `Server.create` instead.
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
        self.register_domain_event(domain_event)

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
        self.register_domain_event(domain_event)

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
        self.register_domain_event(domain_event)

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
        self.register_domain_event(domain_event)

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
        self.register_domain_event(domain_event)

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
        self.register_domain_event(domain_event)

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
            old_value=self._credentials,
            new_value=credentials,
        )
        self._credentials = credentials
        self.register_domain_event(domain_event)

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
        self.register_domain_event(domain_event)

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
        self.register_domain_event(domain_event)

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

    @classmethod
    def create(
        cls,
        name: str,
        cpu: str | None = None,
        ram: str | None = None,
        hdd: str | None = None,
        environment: str | None = None,
        operating_system: dict | None = None,
        credentials: list[dict] | None = None,
        applications: list[dict] | None = None,
    ) -> "Server":
        """Named constructor to create a new Server.

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
            environment=Environment.from_text(environment)
            if environment
            else None,
            operating_system=OperatingSystem.from_data(operating_system)
            if operating_system
            else None,
            credentials=[
                Credential.create(
                    connection_type=credential["connection_type"],
                    username=credential["username"],
                    password=credential["password"],
                    local_ip=credential["local_ip"],
                    local_port=credential["local_port"],
                    public_ip=credential["public_ip"],
                    public_port=credential["public_port"],
                )
                for credential in credentials or []
            ],
            applications=[
                ServerApplication.create(
                    application_id=application["application_id"],
                    install_dir=application["install_dir"],
                    log_dir=application["log_dir"],
                )
                for application in applications or []
            ],
            status="stopped",
            discarded=False,
        )
        domain_event = Server.Created(aggregate_id=server.id.value)
        server.register_domain_event(domain_event)
        return server

    def update(
        self,
        name: str | None = ...,
        cpu: str | None = ...,
        ram: str | None = ...,
        hdd: str | None = ...,
        environment: str | None = ...,
        operating_system: dict | None = ...,
        credentials: list[dict] | None = ...,
        applications: list[dict] | None = ...,
        status: str | None = ...,
        discarded: bool | None = ...,
    ) -> None:
        """Updates the Server.

        Important:
            This method is only used to update an existing Server.
        """
        import ipdb

        ipdb.set_trace()
        if name is not ...:
            self.name = name
        if cpu is not ...:
            self.cpu = cpu
        if ram is not ...:
            self.ram = ram
        if hdd is not ...:
            self.hdd = hdd
        if environment is not ...:
            self.environment = Environment.from_text(environment)
        if operating_system is not ...:
            self.operating_system = OperatingSystem.from_data(operating_system)
        if credentials is not ...:
            self._update_credentials(credentials)
        if applications is not ...:
            self._update_applications(applications)
        if status is not ...:
            self.status = ServerStatus.from_text(status)
        if discarded is not ...:
            self.discarded = discarded

    def _update_credentials(self, credentials: list[dict]) -> None:
        """Updates the credentials of the Server."""
        # Remove credential if not in data.
        for credential in self._credentials:
            if credential.id.value not in [
                new_credential["id"] for new_credential in credentials
            ]:
                self._credentials.remove(credential)
        # Update existing credentials.
        for credential in self._credentials:
            for new_credential in credentials:
                if credential.id.value == new_credential["id"]:
                    credential.update(
                        connection_type=new_credential["connection_type"],
                        username=new_credential["username"],
                        password=new_credential["password"],
                        local_ip=new_credential["local_ip"],
                        local_port=new_credential["local_port"],
                        public_ip=new_credential["public_ip"],
                        public_port=new_credential["public_port"],
                    )
        # Add new credentials.
        for new_credential in credentials:
            if new_credential["id"] not in [
                credential.id.value for credential in self._credentials
            ]:
                self._credentials.append(
                    Credential.create(
                        connection_type=ConnectionType.from_text(
                            new_credential["connection_type"]
                        ),
                        username=new_credential["username"],
                        password=new_credential["password"],
                        local_ip=new_credential["local_ip"],
                        local_port=new_credential["local_port"],
                        public_ip=new_credential["public_ip"],
                        public_port=new_credential["public_port"],
                    )
                )

    def _update_applications(self, applications: list[dict]) -> None:
        """Updates the applications of the Server."""
        # Remove application if not in data.
        for application in self._applications:
            if application.id.value not in [
                new_application["id"] for new_application in applications
            ]:
                self._applications.remove(application)
        # Update existing applications.
        for application in self._applications:
            for new_application in applications:
                if application.id.value == new_application["id"]:
                    application.update(new_application)
        # Add new applications.
        for new_application in applications:
            if new_application["id"] not in [
                application.id.value for application in self._applications
            ]:
                self._applications.append(
                    ServerApplication.create(
                        application_id=new_application["application_id"],
                        install_dir=new_application["install_dir"],
                        log_dir=new_application["log_dir"],
                    )
                )
