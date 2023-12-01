"""Server entity.

This is the aggregate root entity of the Server aggregate.
"""

from st_server.shared.domain.aggregate_root import AggregateRoot
from st_server.shared.domain.domain_event import DomainEvent
from st_server.shared.domain.entity_id import EntityId

from st_server.server.domain.server.connection_type import ConnectionType
from st_server.server.domain.server.credential import Credential
from st_server.server.domain.server.environment import Environment
from st_server.server.domain.server.operating_system import OperatingSystem
from st_server.server.domain.server.server_application import ServerApplication
from st_server.server.domain.server.server_status import ServerStatus


class Server(AggregateRoot):
    """Server entity."""

    class Created(DomainEvent):
        """Domain event that represents the creation of a Server."""

        pass

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
            Use the Server Factory instead.
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

    def update(
        self,
        name: str | None = None,
        cpu: str | None = None,
        ram: str | None = None,
        hdd: str | None = None,
        environment: str | None = None,
        operating_system: dict | None = None,
        credentials: list[dict] | None = None,
        applications: list[dict] | None = None,
        status: str | None = None,
        discarded: bool | None = None,
    ) -> None:
        """Updates the Server.

        Important:
            This method is only used to update an existing Server.
        """
        if name is not None:
            self._name = name
        if cpu is not None:
            self._cpu = cpu
        if ram is not None:
            self._ram = ram
        if hdd is not None:
            self._hdd = hdd
        if environment is not None:
            self._environment = Environment.from_text(environment)
        if operating_system is not None:
            self._operating_system = OperatingSystem.from_data(
                operating_system
            )
        if credentials is not None:
            self._update_credentials(credentials)
        if applications is not None:
            self._update_applications(applications)
        if status is not None:
            self.status = ServerStatus.from_text(status)
        if discarded is not None:
            self.discarded = discarded

    def _update_credentials(self, credentials: list[dict]) -> None:
        """Updates the credentials of the Server."""
        # Remove Credential if not in data.
        for credential in self._credentials:
            if credential.id.value not in [
                new_credential["id"] for new_credential in credentials
            ]:
                self._credentials.remove(credential)
        # Update existing Credentials.
        for credential in self._credentials:
            for new_credential in credentials:
                if credential.id.value == new_credential["id"]:
                    credential.connection_type = ConnectionType.from_text(
                        new_credential["connection_type"]
                    )
                    credential.username = new_credential["username"]
                    credential.password = new_credential["password"]
                    credential.local_ip = new_credential["local_ip"]
                    credential.local_port = new_credential["local_port"]
                    credential.public_ip = new_credential["public_ip"]
                    credential.public_port = new_credential["public_port"]

        # Add new Credentials.
        for new_credential in credentials:
            if new_credential.get("id") is None:
                self._credentials.append(
                    Credential(
                        id=EntityId.generate(),
                        connection_type=ConnectionType.from_text(
                            new_credential["connection_type"]
                        ),
                        username=new_credential["username"],
                        password=new_credential["password"],
                        local_ip=new_credential["local_ip"],
                        local_port=new_credential["local_port"],
                        public_ip=new_credential["public_ip"],
                        public_port=new_credential["public_port"],
                        discarded=False,
                    )
                )

    def _update_applications(self, applications: list[dict]) -> None:
        """Updates the applications of the Server."""
        # Remove Application if not in data.
        for application in self._applications:
            if application.id.value not in [
                new_application["id"] for new_application in applications
            ]:
                self._applications.remove(application)
        # Update existing Applications.
        for application in self._applications:
            for new_application in applications:
                if application.id.value == new_application["id"]:
                    application.update(new_application)
        # Add new Applications.
        for new_application in applications:
            if new_application.get("id") is None:
                self._applications.append(
                    ServerApplication.create(
                        server_id=self._id.value,
                        application_id=new_application["application_id"],
                        install_dir=new_application["install_dir"],
                        log_dir=new_application["log_dir"],
                    )
                )

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
