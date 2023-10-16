"""Credential entity.

This is the aggregate root entity of the credential aggregate.
"""

from st_server.server.domain.value_object.connection_type import (
    ConnectionType,
)
from st_server.shared.domain.entity.entity import Entity
from st_server.shared.domain.value_object.domain_event import DomainEvent
from st_server.shared.domain.value_object.entity_id import EntityId


class Credential(Entity):
    """Credential entity."""

    class ConnectionTypeChanged(DomainEvent):
        """Domain event that represents the change of the connection_type of a Credential."""

        pass

    class UsernameChanged(DomainEvent):
        """Domain event that represents the change of the username of a Credential."""

        pass

    class PasswordChanged(DomainEvent):
        """Domain event that represents the change of the password of a Credential."""

        pass

    class LocalIpChanged(DomainEvent):
        """Domain event that represents the change of the local_ip of a Credential."""

        pass

    class LocalPortChanged(DomainEvent):
        """Domain event that represents the change of the local_port of a Credential."""

        pass

    class PublicIpChanged(DomainEvent):
        """Domain event that represents the change of the public_ip of a Credential."""

        pass

    class PublicPortChanged(DomainEvent):
        """Domain event that represents the change of the public_port of a Credential."""

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
        """Initializes the Credential.

        Important:
            Do not use directly to create a new Credential.
            Use the named constructor `Credential.create` instead.
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
        """Returns the server id of the Credential."""
        return self._server_id

    @server_id.setter
    def server_id(self, server_id: EntityId) -> None:
        """Sets the server id of the Credential."""
        self._check_not_discarded()
        self._server_id = server_id

    @property
    def connection_type(self) -> ConnectionType:
        """Returns the connection type of the Credential."""
        return self._connection_type

    @connection_type.setter
    def connection_type(self, connection_type: ConnectionType) -> None:
        """Sets the connection type of the Credential."""
        self._check_not_discarded()
        self._connection_type = connection_type

    @property
    def username(self) -> str:
        """Returns the username of the Credential."""
        return self._username

    @username.setter
    def username(self, username: str) -> None:
        """Sets the username of the Credential."""
        self._check_not_discarded()
        self._username = username

    @property
    def password(self) -> str:
        """Returns the password of the Credential."""
        return self._password

    @password.setter
    def password(self, password: str) -> None:
        """Sets the password of the Credential."""
        self._check_not_discarded()
        self._password = password

    @property
    def local_ip(self) -> str:
        """Returns the local ip of the Credential."""
        return self._local_ip

    @local_ip.setter
    def local_ip(self, local_ip: str) -> None:
        """Sets the local ip of the Credential."""
        self._check_not_discarded()
        self._local_ip = local_ip

    @property
    def local_port(self) -> int:
        """Returns the local port of the Credential."""
        return self._local_port

    @local_port.setter
    def local_port(self, local_port: int) -> None:
        """Sets the local port of the Credential."""
        self._check_not_discarded()
        self._local_port = local_port

    @property
    def public_ip(self) -> str:
        """Returns the public ip of the Credential."""
        return self._public_ip

    @public_ip.setter
    def public_ip(self, public_ip: str) -> None:
        """Sets the public ip of the Credential."""
        self._check_not_discarded()
        self._public_ip = public_ip

    @property
    def public_port(self) -> int:
        """Returns the public port of the Credential."""
        return self._public_port

    @public_port.setter
    def public_port(self, public_port: int) -> None:
        """Sets the public port of the Credential."""
        self._check_not_discarded()
        self._public_port = public_port

    def __repr__(self) -> str:
        """Returns the representation of the Credential."""
        return (
            "{d}{c}(id={id!r}, "
            "connection_type={connection_type!r}, "
            "username={username!r}, password={password!r}, "
            "local_ip={local_ip!r}, local_port={local_port!r}, "
            "public_ip={public_ip!r}, public_port={public_port!r}, "
            "discarded={discarded!r})"
        ).format(
            d="*Discarded* " if self._discarded else "",
            c=self.__class__.__name__,
            id=self._id.value,
            connection_type=self._connection_type.value,
            username=self._username,
            password=self._password,
            local_ip=self._local_ip,
            local_port=self._local_port,
            public_ip=self._public_ip,
            public_port=self._public_port,
            discarded=self._discarded,
        )

    @classmethod
    def create(
        cls,
        connection_type: ConnectionType,
        username: str,
        password: str,
        local_ip: str | None = None,
        local_port: int | None = None,
        public_ip: str | None = None,
        public_port: int | None = None,
    ) -> "Credential":
        """Named constructor to create a new Credential.

        Important:
            This method is only used to create a new Credential.
            When creating a new Credential, the id is automatically generated
            and a domain event is registered.
        """
        return cls(
            id=EntityId.generate(),
            connection_type=connection_type,
            username=username,
            password=password,
            local_ip=local_ip,
            local_port=local_port,
            public_ip=public_ip,
            public_port=public_port,
            discarded=False,
        )

    def update(
        self,
        connection_type: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        local_ip: str | None = ...,
        local_port: int | None = ...,
        public_ip: str | None = ...,
        public_port: int | None = ...,
        discarded: bool | None = ...,
    ) -> None:
        """Updates the Credential.

        Important:
            This method is only used to update an existing Credential.
        """
        if connection_type is not ...:
            self.connection_type = ConnectionType.from_text(connection_type)
        if username is not ...:
            self.username = username
        if password is not ...:
            self.password = password
        if local_ip is not ...:
            self.local_ip = local_ip
        if local_port is not ...:
            self.local_port = local_port
        if public_ip is not ...:
            self.public_ip = public_ip
        if public_port is not ...:
            self.public_port = public_port
        if discarded is not ...:
            self.discarded = discarded
