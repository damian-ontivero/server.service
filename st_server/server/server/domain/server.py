from st_server.server.server.domain.connection_type import ConnectionType
from st_server.server.server.domain.credential import Credential
from st_server.server.server.domain.environment import Environment
from st_server.server.server.domain.operating_system import OperatingSystem
from st_server.server.server.domain.server_application import ServerApplication
from st_server.server.server.domain.server_status import ServerStatus
from st_server.shared.domain.aggregate_root import AggregateRoot
from st_server.shared.domain.domain_event import DomainEvent
from st_server.shared.domain.entity_id import EntityId


class Server(AggregateRoot):
    class Registered(DomainEvent):
        pass

    def __init__(
        self,
        id: EntityId,
        name: str,
        cpu: str,
        ram: str,
        hdd: str,
        environment: Environment,
        operating_system: OperatingSystem,
        credentials: list[Credential],
        applications: list[ServerApplication],
        status: ServerStatus,
        discarded: bool,
    ) -> None:
        """
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

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._check_not_discarded()
        self._name = name
        self._register_domain_event(
            Server.Modified(
                aggregate_id=self._id.value,
                old_value=self._name,
                new_value=name,
            )
        )

    @property
    def cpu(self) -> str:
        return self._cpu

    @cpu.setter
    def cpu(self, cpu: str) -> None:
        self._check_not_discarded()
        self._cpu = cpu
        self._register_domain_event(
            Server.Modified(
                aggregate_id=self._id.value,
                old_value=self._cpu,
                new_value=cpu,
            )
        )

    @property
    def ram(self) -> str:
        return self._ram

    @ram.setter
    def ram(self, ram: str) -> None:
        self._check_not_discarded()
        self._ram = ram
        self._register_domain_event(
            Server.Modified(
                aggregate_id=self._id.value,
                old_value=self._ram,
                new_value=ram,
            )
        )

    @property
    def hdd(self) -> str:
        return self._hdd

    @hdd.setter
    def hdd(self, hdd: str) -> None:
        self._check_not_discarded()
        self._hdd = hdd
        self._register_domain_event(
            Server.Modified(
                aggregate_id=self._id.value,
                old_value=self._hdd,
                new_value=hdd,
            )
        )

    @property
    def environment(self) -> Environment:
        return self._environment

    @environment.setter
    def environment(self, environment: Environment) -> None:
        self._check_not_discarded()
        self._environment = environment
        self._register_domain_event(
            Server.Modified(
                aggregate_id=self._id.value,
                old_value=self._environment.value,
                new_value=environment.value,
            )
        )

    @property
    def operating_system(self) -> OperatingSystem:
        return self._operating_system

    @operating_system.setter
    def operating_system(self, operating_system: OperatingSystem) -> None:
        self._check_not_discarded()
        self._operating_system = operating_system
        self._register_domain_event(
            Server.Modified(
                aggregate_id=self._id.value,
                old_value=self._operating_system.__dict__,
                new_value=operating_system.__dict__,
            )
        )

    @property
    def credentials(self) -> list[Credential]:
        return self._credentials

    @credentials.setter
    def credentials(self, credentials: list[Credential]) -> None:
        self._check_not_discarded()
        self._credentials = credentials
        self._register_domain_event(
            Server.Modified(
                aggregate_id=self._id.value,
                old_value=self._credentials,
                new_value=credentials,
            )
        )

    @property
    def applications(self) -> list[ServerApplication]:
        return self._applications

    @applications.setter
    def applications(self, applications: list[ServerApplication]) -> None:
        self._check_not_discarded()
        self._applications = applications
        self._register_domain_event(
            Server.Modified(
                aggregate_id=self._id.value,
                old_value=self._applications,
                new_value=applications,
            )
        )

    @property
    def status(self) -> ServerStatus:
        return self._status

    @status.setter
    def status(self, status: ServerStatus) -> None:
        self._check_not_discarded()
        self._status = status
        self._register_domain_event(
            Server.Modified(
                aggregate_id=self._id.value,
                old_value=self._status.value,
                new_value=status.value,
            )
        )

    @classmethod
    def register(
        cls,
        name: str,
        cpu: str,
        ram: str,
        hdd: str,
        environment: str,
        operating_system: dict,
        credentials: list[dict],
        applications: list[dict],
    ):
        server = cls(
            id=EntityId.generate(),
            name=name,
            cpu=cpu,
            ram=ram,
            hdd=hdd,
            environment=Environment.from_text(environment),
            operating_system=OperatingSystem.from_data(operating_system),
            credentials=[
                Credential(
                    id=EntityId.generate(),
                    server_id=EntityId.generate(),
                    connection_type=ConnectionType.from_text(
                        credential["connection_type"]
                    ),
                    username=credential["username"],
                    password=credential["password"],
                    local_ip=credential["local_ip"],
                    local_port=credential["local_port"],
                    public_ip=credential["public_ip"],
                    public_port=credential["public_port"],
                    discarded=False,
                )
                for credential in credentials
            ],
            applications=[
                ServerApplication.from_data(application)
                for application in applications
            ],
            status=ServerStatus.from_text("stopped"),
            discarded=False,
        )
        server._register_domain_event(
            Server.Registered(aggregate_id=server.id.value)
        )
        return server

    @classmethod
    def from_primitive_values(
        cls,
        id: str,
        name: str,
        cpu: str,
        ram: str,
        hdd: str,
        environment: str,
        operating_system: dict,
        credentials: list[dict],
        applications: list[dict],
        status: str,
        discarded: bool,
    ):
        return cls(
            id=EntityId.from_text(id),
            name=name,
            cpu=cpu,
            ram=ram,
            hdd=hdd,
            environment=Environment.from_text(environment),
            operating_system=OperatingSystem.from_data(operating_system),
            credentials=[
                Credential(
                    id=EntityId.from_text(credential["id"]),
                    server_id=EntityId.from_text(credential["server_id"]),
                    connection_type=ConnectionType.from_text(
                        credential["connection_type"]
                    ),
                    username=credential["username"],
                    password=credential["password"],
                    local_ip=credential["local_ip"],
                    local_port=credential["local_port"],
                    public_ip=credential["public_ip"],
                    public_port=credential["public_port"],
                    discarded=credential["discarded"],
                )
                for credential in credentials
            ],
            applications=[
                ServerApplication.from_data(application)
                for application in applications
            ],
            status=ServerStatus.from_text(status),
            discarded=discarded,
        )

    def discard(self) -> None:
        self._check_not_discarded()
        self._discarded = True
        self._register_domain_event(
            Server.Discarded(aggregate_id=self._id.value)
        )
