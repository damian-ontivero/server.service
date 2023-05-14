"""Server entity.

This is the aggregate root entity of the server aggregate.
"""

from st_server.domain.aggregate_root import AggregateRoot
from st_server.domain.domain_event import DomainEvent
from st_server.domain.entity_id import EntityId
from st_server.domain.server.credential import Credential
from st_server.domain.server.environment import Environment
from st_server.domain.server.operating_system import OperatingSystem
from st_server.domain.server.server_application import ServerApplication


class Server(AggregateRoot):
    """Server entity."""

    class NameChanged(DomainEvent):
        """Domain event for name changed."""

        pass

    class CpuChanged(DomainEvent):
        """Domain event for cpu changed."""

        pass

    class RamChanged(DomainEvent):
        """Domain event for ram changed."""

        pass

    class HddChanged(DomainEvent):
        """Domain event for hdd changed."""

        pass

    class EnvironmentChanged(DomainEvent):
        """Domain event for environment changed."""

        pass

    class OperatingSystemChanged(DomainEvent):
        """Domain event for operating system changed."""

        pass

    class CredentialChanged(DomainEvent):
        """Domain event for credential changed."""

        pass

    class ApplicationChanged(DomainEvent):
        """Domain event for applications changed."""

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
        discarded: bool | None = None,
    ) -> None:
        """Constructor of the server entity.

        Important:
            This constructor should not be used directly to generate the entity.
            It should be used only by the repository to instantiate the entity from the database.

            In order to create/generate/register a new server, use the `Server.create` method.

        Args:
            id (`EntityId`): Server id.
            name (`str`): Server name.
            cpu (`str`): Server cpu.
            ram (`str`): Server ram.
            hdd (`str`): Server hdd.
            environment (`Environment`): Server environment.
            operating_system (`OperatingSystem`): Server operating system.
            credentials (`list[Credential]`): Server credentials.
            applications (`list[ServerApplication]`): Server applications.
            discarded (`bool`): Indicates if the server is discarded.
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

    @property
    def name(self) -> str:
        """Returns the name of the server.

        Returns:
            `str`: Name of the server.
        """
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Sets the name of the server.

        Args:
            value (`str`): Name of the server.
        """
        if self._name == value:
            return

        domain_event = Server.NameChanged(
            type_="server_updated",
            aggregate_id=self.id,
            old_value=self._name,
            new_value=value,
        )

        self._name = value
        self.register_domain_event(domain_event=domain_event)

    @property
    def cpu(self) -> str:
        """Returns the cpu of the server.

        Returns:
            `str`: Cpu of the server.
        """
        return self._cpu

    @cpu.setter
    def cpu(self, value: str) -> None:
        """Sets the cpu of the server.

        Args:
            value (`str`): Cpu of the server.
        """
        if self._cpu == value:
            return

        domain_event = Server.CpuChanged(
            type_="server_updated",
            aggregate_id=self.id,
            old_value=self._cpu,
            new_value=value,
        )

        self._cpu = value
        self.register_domain_event(domain_event=domain_event)

    @property
    def ram(self) -> str:
        """Returns the ram of the server.

        Returns:
            `str`: Ram of the server.
        """
        return self._ram

    @ram.setter
    def ram(self, value: str) -> None:
        """Sets the ram of the server.

        Args:
            value (`str`): Ram of the server.
        """
        if self._ram == value:
            return

        domain_event = Server.RamChanged(
            type_="server_updated",
            aggregate_id=self.id,
            old_value=self._ram,
            new_value=value,
        )

        self._ram = value
        self.register_domain_event(domain_event=domain_event)

    @property
    def hdd(self) -> str:
        """Returns the hdd of the server.

        Returns:
            `str`: Hdd of the server.
        """
        return self._hdd

    @hdd.setter
    def hdd(self, value: str) -> None:
        """Sets the hdd of the server.

        Args:
            value (`str`): Hdd of the server.
        """
        if self._hdd == value:
            return

        domain_event = Server.HddChanged(
            type_="server_updated",
            aggregate_id=self.id,
            old_value=self._hdd,
            new_value=value,
        )

        self._hdd = value
        self.register_domain_event(domain_event=domain_event)

    @property
    def environment(self) -> Environment:
        """Returns the environment of the server.

        Returns:
            `Environment`: Environment of the server.
        """
        return self._environment

    @environment.setter
    def environment(self, value: Environment) -> None:
        """Sets the environment of the server.

        Args:
            value (`Environment`): Environment of the server.
        """
        if self._environment == value:
            return

        domain_event = Server.EnvironmentChanged(
            type_="server_updated",
            aggregate_id=self.id,
            old_value=self._environment,
            new_value=value,
        )

        self._environment = value
        self.register_domain_event(domain_event=domain_event)

    @property
    def operating_system(self) -> OperatingSystem:
        """Returns the operating system of the server.

        Returns:
            `OperatingSystem`: Operating system of the server.
        """
        return self._operating_system

    @operating_system.setter
    def operating_system(self, value: OperatingSystem) -> None:
        """Sets the operating system of the server.

        Args:
            value (`OperatingSystem`): Operating system of the server.
        """
        if self._operating_system == value:
            return

        domain_event = Server.OperatingSystemChanged(
            type_="server_updated",
            aggregate_id=self.id,
            old_value=self._operating_system,
            new_value=value,
        )

        self._operating_system = value
        self.register_domain_event(domain_event=domain_event)

    @property
    def credentials(self) -> list[Credential]:
        """Returns the credentials of the server.

        Returns:
            `list[Credential]`: Credentials of the server.
        """
        return self._credentials

    @credentials.setter
    def credentials(self, value: list[Credential]) -> None:
        """Sets the credentials of the server.

        Args:
            value (`list[Credential]`): Credentials of the server.
        """
        if self._credentials == value:
            return

        domain_event = Server.CredentialChanged(
            type_="server_updated",
            aggregate_id=self.id,
            old_value=self._credentials,
            new_value=value,
        )

        self._credentials = value
        self.register_domain_event(domain_event=domain_event)

    @property
    def applications(self) -> list[ServerApplication]:
        """Returns the applications of the server.

        Returns:
            `list[ServerApplication]`: Applications of the server.
        """
        return self._applications

    @applications.setter
    def applications(self, value: list[ServerApplication]) -> None:
        """Sets the applications of the server.

        Args:
            value (`list[ServerApplication]`): Applications of the server.
        """
        if self._applications == value:
            return

        domain_event = Server.ApplicationChanged(
            type_="server_updated",
            aggregate_id=self.id,
            old_value=self._applications,
            new_value=value,
        )

        self._applications = value
        self.register_domain_event(domain_event=domain_event)

    def __repr__(self) -> str:
        """Returns the string representation of the object.

        Returns:
            `str`: String representation of the object.
        """
        return (
            f"{self.__class__.__name__}(id={self.id}, "
            f"name={self._name}, cpu={self._cpu}, "
            f"ram={self._ram}, hdd={self._hdd}, "
            f"environment={self._environment}, "
            f"operating_system={self._operating_system}, "
            f"applications={self._applications}, "
            f"credentials={self._credentials}, "
            f"discarded={self._discarded})"
        )

    def to_dict(self) -> dict:
        """Returns a dictionary representation of the object.

        Returns:
            `dict`: Dictionary representation of the object.
        """
        return {
            "id": self.id,
            "name": self._name,
            "cpu": self._cpu,
            "ram": self._ram,
            "hdd": self._hdd,
            "environment": self._environment,
            "operating_system": self._operating_system,
            "credentials": [
                credential.to_dict() for credential in self._credentials
            ],
            "applications": [
                application.to_dict() for application in self._applications
            ],
            "discarded": self._discarded,
        }

    @staticmethod
    def from_dict(data: dict) -> "Server":
        """Returns an instance of the class based on the provided dictionary.

        Args:
            data (`dict`): Dictionary representation of the object.

        Returns:
            `Server`: Instance of the class.
        """
        for k, v in data.items():
            if k == "credentials":
                data[k] = [
                    Credential.from_dict(data=credential) for credential in v
                ]
            elif k == "applications":
                data[k] = [
                    ServerApplication.from_dict(data=application)
                    for application in v
                ]

        return Server(**data)

    @staticmethod
    def create(
        name: str,
        cpu: str,
        ram: str,
        hdd: str,
        environment: Environment,
        operating_system: OperatingSystem,
        credentials: list[Credential] | None = None,
        applications: list[ServerApplication] | None = None,
    ) -> "Server":
        """Server factory method.

        Important:
            This method is only used to create a new server.
            When creating a new server, the id is automatically generated
            and a domain event is registered.

        Args:
            name (`str`): Server name.
            cpu (`str`): Server cpu.
            ram (`str`): Server ram.
            hdd (`str`): Server hdd.
            environment (`Environment`): Server environment.
            operating_system (`OperatingSystem`): Server operating system.
            credentials (`list[Credential]`): Server credentials.
            applications (`list[ServerApplication]`): Server applications.

        Returns:
            `Server`: Server instance.
        """
        server = Server(
            id=EntityId().value,
            name=name,
            cpu=cpu,
            ram=ram,
            hdd=hdd,
            environment=environment,
            operating_system=operating_system,
            credentials=credentials,
            applications=applications,
        )

        domain_event = Server.Created(
            type_="server_created", aggregate_id=server.id
        )
        server.register_domain_event(domain_event=domain_event)

        return server

    def discard(self) -> None:
        """Server discard method.

        Important:
            This method is only used to discard an server.
            When discarding an server, the discarded attribute is set to True
            and a domain event is registered.
        """
        domain_event = Server.Discarded(
            type_="server_discarded", aggregate_id=self._id
        )

        self._discarded = True
        self.register_domain_event(domain_event=domain_event)
