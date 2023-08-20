"""Credential entity.

This is the aggregate root entity of the credential aggregate.
"""

from st_server.server.domain.value_objects.connection_type import (
    ConnectionType,
)
from st_server.shared.domain.entities.entity import Entity
from st_server.shared.domain.value_objects.domain_event import DomainEvent
from st_server.shared.domain.value_objects.entity_id import EntityId


class Credential(Entity):
    """Credential entity."""

    class Created(DomainEvent):
        pass

    class Discarded(DomainEvent):
        pass

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
        """
        Important:
            Do not use directly to create a new Credential.
            Use the factory method `Credential.create` instead.
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
        return self._server_id

    @server_id.setter
    def server_id(self, server_id: EntityId) -> None:
        self._check_not_discarded()
        self._server_id = server_id

    @property
    def connection_type(self) -> ConnectionType:
        return self._connection_type

    @connection_type.setter
    def connection_type(self, connection_type: ConnectionType) -> None:
        self._check_not_discarded()
        self._connection_type = connection_type

    @property
    def username(self) -> str:
        return self._username

    @username.setter
    def username(self, username: str) -> None:
        self._check_not_discarded()
        self._username = username

    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, password: str) -> None:
        self._check_not_discarded()
        self._password = password

    @property
    def local_ip(self) -> str:
        return self._local_ip

    @local_ip.setter
    def local_ip(self, local_ip: str) -> None:
        self._check_not_discarded()
        self._local_ip = local_ip

    @property
    def local_port(self) -> int:
        return self._local_port

    @local_port.setter
    def local_port(self, local_port: int) -> None:
        self._check_not_discarded()
        self._local_port = local_port

    @property
    def public_ip(self) -> str:
        return self._public_ip

    @public_ip.setter
    def public_ip(self, public_ip: str) -> None:
        self._check_not_discarded()
        self._public_ip = public_ip

    @property
    def public_port(self) -> int:
        return self._public_port

    @public_port.setter
    def public_port(self, public_port: int) -> None:
        self._check_not_discarded()
        self._public_port = public_port

    def __repr__(self) -> str:
        return (
            "{d}{c}(id={id!r}, server_id={server_id!r}, "
            "connection_type={connection_type!r}, "
            "username={username!r}, password={password!r}, "
            "local_ip={local_ip!r}, local_port={local_port!r}, "
            "public_ip={public_ip!r}, public_port={public_port!r}, "
            "discarded={discarded!r})"
        ).format(
            d="*Discarded* " if self._discarded else "",
            c=self.__class__.__name__,
            id=self._id.value,
            server_id=self._server_id.value,
            connection_type=self._connection_type.value,
            username=self._username,
            password=self._password,
            local_ip=self._local_ip,
            local_port=self._local_port,
            public_ip=self._public_ip,
            public_port=self._public_port,
            discarded=self._discarded,
        )

    def to_dict(self) -> dict:
        return {
            "id": self._id.value,
            "server_id": self._server_id.value,
            "connection_type": self._connection_type.value,
            "username": self._username,
            "password": self._password,
            "local_ip": self._local_ip,
            "local_port": self._local_port,
            "public_ip": self._public_ip,
            "public_port": self._public_port,
            "discarded": self._discarded,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Credential":
        return cls(
            id=EntityId.from_string(value=data.get("id"))
            if data.get("id")
            else EntityId.generate(),
            server_id=EntityId.from_string(value=data.get("server_id")),
            connection_type=ConnectionType.from_string(
                value=data.get("connection_type")
            ),
            username=data.get("username"),
            password=data.get("password"),
            local_ip=data.get("local_ip"),
            local_port=data.get("local_port"),
            public_ip=data.get("public_ip"),
            public_port=data.get("public_port"),
            discarded=data.get("discarded"),
        )

    @classmethod
    def create(
        cls,
        server_id: EntityId,
        connection_type: ConnectionType,
        username: str,
        password: str,
        local_ip: str,
        local_port: int,
        public_ip: str,
        public_port: int,
    ) -> "Credential":
        """
        Important:
            This method is only used to create a new credential.
            When creating a new credential, the id is automatically generated
            and a domain event is registered.
        """
        return cls(
            id=EntityId.generate(),
            server_id=server_id,
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
        server_id: EntityId | None = None,
        connection_type: ConnectionType | None = None,
        username: str | None = None,
        password: str | None = None,
        local_ip: str | None = None,
        local_port: int | None = None,
        public_ip: str | None = None,
        public_port: int | None = None,
    ) -> None:
        """
        Important:
            This method is only used to update an credential.
            When updating the attributes, the domain events
            are registered by setters.
        """
        if server_id is not None and not server_id == self._server_id:
            self.server_id = server_id
        if (
            connection_type is not None
            and not connection_type == self._connection_type
        ):
            self.connection_type = connection_type
        if username is not None and not username == self._username:
            self.username = username
        if password is not None and not password == self._password:
            self.password = password
        if local_ip is not None and not local_ip == self._local_ip:
            self.local_ip = local_ip
        if local_port is not None and not local_port == self._local_port:
            self.local_port = local_port
        if public_ip is not None and not public_ip == self._public_ip:
            self.public_ip = public_ip
        if public_port is not None and not public_port == self._public_port:
            self.public_port = public_port
        return self

    def discard(self) -> None:
        """
        Important:
            This method is only used to discard an credential.
            When discarding an credential, the discarded attribute is set to True
            and a domain event is registered.
        """
        self._discarded = True
