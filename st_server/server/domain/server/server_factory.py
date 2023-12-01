from st_server.shared.domain.entity_id import EntityId
from st_server.shared.domain.factory import Factory

from st_server.server.domain.server.connection_type import ConnectionType
from st_server.server.domain.server.credential import Credential
from st_server.server.domain.server.environment import Environment
from st_server.server.domain.server.operating_system import OperatingSystem
from st_server.server.domain.server.server import Server
from st_server.server.domain.server.server_application import ServerApplication
from st_server.server.domain.server.server_status import ServerStatus


class ServerFactory(Factory):
    """Server Factory.

    This Factory is used to build a complete new Server or rebuild an existing Server.
    """

    @staticmethod
    def build(
        name: str,
        cpu: str | None = None,
        ram: str | None = None,
        hdd: str | None = None,
        environment: str | None = None,
        operating_system: dict | None = None,
        credentials: list[dict] | None = None,
        applications: list[dict] | None = None,
    ) -> Server:
        """Builds a new Server.

        Important:
            This method is only used to build a new Server.
            When building a new Server, the id is automatically generated
            and a domain event is registered.
        """
        server = Server(
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
                Credential(
                    id=EntityId.generate(),
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
                for credential in credentials or []
            ],
            applications=[
                ServerApplication(
                    application_id=EntityId.from_text(
                        application["application_id"]
                    ),
                    install_dir=application["install_dir"],
                    log_dir=application["log_dir"],
                )
                for application in applications or []
            ],
            status=ServerStatus.from_text("stopped"),
            discarded=False,
        )
        domain_event = Server.Created(aggregate_id=server.id.value)
        server.register_domain_event(domain_event)
        return server

    @staticmethod
    def rebuild(
        id: str,
        name: str,
        cpu: str | None = None,
        ram: str | None = None,
        hdd: str | None = None,
        environment: str | None = None,
        operating_system: dict | None = None,
        credentials: list[dict] | None = None,
        applications: list[dict] | None = None,
        status: str | None = None,
        discarded: bool | None = None,
    ) -> Server:
        """Rebuilds an existing Server.

        Important:
            This method is only used to rebuild a Server.
            When rebuilding a Server, the id is not generated
            and a domain event is not registered.
        """
        server = Server(
            id=EntityId.from_text(id),
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
                Credential(
                    id=EntityId.from_text(credential["id"]),
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
                for credential in credentials or []
            ],
            applications=[
                ServerApplication(
                    application_id=EntityId.from_text(
                        application["application_id"]
                    ),
                    install_dir=application["install_dir"],
                    log_dir=application["log_dir"],
                )
                for application in applications or []
            ],
            status=ServerStatus.from_text(status) if status else None,
            discarded=discarded,
        )
        return server
