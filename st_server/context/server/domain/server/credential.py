"""Credential entity.

This is the aggregate root entity of the credential aggregate.
"""

from st_server.context.server.domain.connection_type.connection_type import (
    ConnectionType,
)
from st_server.shared.core.domain_event import DomainEvent
from st_server.shared.core.entity import Entity
from st_server.shared.core.entity_id import EntityId


class Credential(Entity):
    """Credential entity."""

    class ServerIdChanged(DomainEvent):
        pass

    class ConnectionTypeChanged(DomainEvent):
        pass

    class UsernameChanged(DomainEvent):
        pass

    class PasswordChanged(DomainEvent):
        pass

    class LocalIpChanged(DomainEvent):
        pass

    class LocalPortChanged(DomainEvent):
        pass

    class PublicIpChanged(DomainEvent):
        pass

    class PublicPortChanged(DomainEvent):
        pass

    def __init__(
        self,
        id: EntityId | None = None,
        server_id: EntityId | None = None,
        connection_type: ConnectionType | None = None,
        username: str | None = None,
        password: str | None = None,
        local_ip: str | None = None,
        local_port: str | None = None,
        public_ip: str | None = None,
        public_port: str | None = None,
        discarded: bool | None = None,
    ) -> None:
        """Constructor of the credential entity.

        Important:
            This constructor should not be used directly to generate the entity.
            It should be used only by the repository to instantiate the entity from the database.

            In order to create/generate/register a new credential, use the `Credential.create` method.

        Args:
            id (`EntityId`): Credential id.
            server_id (`EntityId`): Server id.
            connection_type (`EntityId`): Connection type id.
            username (`str`): Credential username.
            password (`str`): Credential password.
            local_ip (`str`): Credential local ip.
            local_port (`str`): Credential local port.
            public_ip (`str`): Credential public ip.
            public_port (`str`): Credential public port.
            discarded (`bool`): Indicates if the credential is discarded.
        """
        super().__init__(id=id, discarded=discarded)
        self._server_id = server_id
        self._connection_type = connection_type
        self._username = username
        self._password = password
        self._local_ip = local_ip
        self._local_port = local_port
        self._public_ip = public_ip
        self._public_port = public_port

    @property
    def server_id(self) -> EntityId:
        """Returns the server id of the credential.

        Returns:
            `EntityId`: Server id of the credential.
        """
        return self._server_id

    @server_id.setter
    def server_id(self, value: EntityId) -> None:
        """Sets the server id of the credential.

        Args:
            value (`EntityId`): Server id of the credential.
        """
        if self._server_id == value:
            return

        domain_event = Credential.ServerIdChanged(
            type_="credential_updated",
            aggregate_id=self.id,
            old_value=self._server_id,
            new_value=value,
        )

        self._server_id = value
        self.register_domain_event(domain_event=domain_event)

    @property
    def connection_type(self) -> ConnectionType:
        """Returns the connection type of the credential.

        Returns:
            `ConnectionType`: Connection type of the credential.
        """
        return self._connection_type

    @connection_type.setter
    def connection_type(self, value: ConnectionType) -> None:
        """Sets the connection type of the credential.

        Args:
            value (`ConnectionType`): Connection type of the credential.
        """
        if self._connection_type == value:
            return

        domain_event = Credential.ConnectionTypeChanged(
            type_="credential_updated",
            aggregate_id=self.id,
            old_value=self._connection_type,
            new_value=value,
        )

        self._connection_type = value
        self.register_domain_event(domain_event=domain_event)

    @property
    def username(self) -> str:
        """Returns the username of the credential.

        Returns:
            `str`: Username of the credential.
        """
        return self._username

    @username.setter
    def username(self, value: str) -> None:
        """Sets the username of the credential.

        Args:
            value (`str`): Username of the credential.
        """
        if self._username == value:
            return

        domain_event = Credential.UsernameChanged(
            type_="credential_updated",
            aggregate_id=self.id,
            old_value=self._username,
            new_value=value,
        )

        self._username = value
        self.register_domain_event(domain_event=domain_event)

    @property
    def password(self) -> str:
        """Returns the password of the credential.

        Returns:
            `str`: Password of the credential.
        """
        return self._password

    @password.setter
    def password(self, value: str) -> None:
        """Sets the password of the credential.

        Args:
            value (`str`): Password of the credential.
        """
        if self._password == value:
            return

        domain_event = Credential.PasswordChanged(
            type_="credential_updated",
            aggregate_id=self.id,
            old_value=self._password,
            new_value=value,
        )

        self._password = value
        self.register_domain_event(domain_event=domain_event)

    @property
    def local_ip(self) -> str:
        """Returns the local ip of the credential.

        Returns:
            `str`: Local ip of the credential.
        """
        return self._local_ip

    @local_ip.setter
    def local_ip(self, value: str) -> None:
        """Sets the local ip of the credential.

        Args:
            value (`str`): Local ip of the credential.
        """
        if self._local_ip == value:
            return

        domain_event = Credential.LocalIpChanged(
            type_="credential_updated",
            aggregate_id=self.id,
            old_value=self._local_ip,
            new_value=value,
        )

        self._local_ip = value
        self.register_domain_event(domain_event=domain_event)

    @property
    def local_port(self) -> int:
        """Returns the local port of the credential.

        Returns:
            `int`: Local port of the credential.
        """
        return self._local_port

    @local_port.setter
    def local_port(self, value: int) -> None:
        """Sets the local port of the credential.

        Args:
            value (`int`): Local port of the credential.
        """
        if self._local_port == value:
            return

        domain_event = Credential.LocalPortChanged(
            type_="credential_updated",
            aggregate_id=self.id,
            old_value=self._local_port,
            new_value=value,
        )

        self._local_port = value
        self.register_domain_event(domain_event=domain_event)

    def __repr__(self) -> str:
        """Returns the string representation of the object.

        Returns:
            `str`: String representation of the object.
        """
        return (
            "{d}{c}(id={id!r}, server_id={server_id!r}, connection_type={connection_type!r}, "
            "username={username!r}, password={password!r}, local_ip={local_ip!r}, "
            "local_port={local_port!r}, public_ip={public_ip!r}, public_port={public_port!r}, "
            "discarded={discarded!r})"
        ).format(
            d="*Discarded* " if self._discarded else "",
            c=self.__class__.__name__,
            id=self.id,
            server_id=self._server_id,
            connection_type=self._connection_type,
            username=self._username,
            password=self._password,
            local_ip=self._local_ip,
            local_port=self._local_port,
            public_ip=self._public_ip,
            public_port=self._public_port,
            discarded=self._discarded,
        )

    def to_dict(self) -> dict:
        """Returns a dictionary representation of the object.

        Returns:
            `dict`: Dictionary representation of the object.
        """
        return {
            "id": self.id,
            "server_id": self._server_id,
            "connection_type": self._connection_type,
            "username": self._username,
            "password": self._password,
            "local_ip": self._local_ip,
            "local_port": self._local_port,
            "public_ip": self._public_ip,
            "public_port": self._public_port,
            "discarded": self._discarded,
        }

    @staticmethod
    def from_dict(data: dict) -> "Credential":
        """Returns an instance of the class based on the provided dictionary.

        Args:
            data (`dict`): Dictionary representation of the object.

        Returns:
            `Credential`: Instance of the class.
        """
        return Credential(**data)

    @staticmethod
    def create(
        username: str,
        password: str,
        local_ip: str,
        local_port: int,
        public_ip: str,
        public_port: int,
    ) -> "Credential":
        """Credential factory method.

        Important:
            This method is only used to create a new credential.
            When creating a new credential, the id is automatically generated
            and a domain event is registered.

        Args:
            username (`str`): Username of the credential.
            password (`str`): Password of the credential.
            local_ip (`str`): Local ip of the credential.
            local_port (`int`): Local port of the credential.
            public_ip (`str`): Public ip of the credential.
            public_port (`int`): Public port of the credential.

        Returns:
            `Credential`: Credential instance.
        """
        credential = Credential(
            id=EntityId(),
            username=username,
            password=password,
            local_ip=local_ip,
            local_port=local_port,
            public_ip=public_ip,
            public_port=public_port,
            discarded=False,
        )

        domain_event = Credential.Created(
            type_="credential_created", aggregate_id=credential.id
        )
        credential.register_domain_event(domain_event=domain_event)

        return credential

    def discard(self) -> None:
        """Credential discard method.

        Important:
            This method is only used to discard an credential.
            When discarding an credential, the discarded attribute is set to True
            and a domain event is registered.
        """
        domain_event = Credential.Discarded(
            type_="credential_discarded", aggregate_id=self._id
        )

        self._discarded = True
        self.register_domain_event(domain_event=domain_event)
