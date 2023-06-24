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
    def server_id(self) -> str:
        return self._server_id.value

    @server_id.setter
    def server_id(self, value: str) -> None:
        self._check_not_discarded()
        server_id = EntityId.from_string(value=value)
        domain_event = Credential.ServerIdChanged(
            aggregate_id=self._id.value,
            old_value=self._server_id.value,
            new_value=server_id.value,
        )
        self._server_id = server_id
        self.register_domain_event(domain_event=domain_event)

    @property
    def connection_type(self) -> ConnectionType:
        return self._connection_type

    @connection_type.setter
    def connection_type(self, value: ConnectionType) -> None:
        self._check_not_discarded()
        domain_event = Credential.ConnectionTypeChanged(
            aggregate_id=self._id.value,
            old_value=self._connection_type,
            new_value=value,
        )
        self._connection_type = value
        self.register_domain_event(domain_event=domain_event)

    @property
    def username(self) -> str:
        return self._username

    @username.setter
    def username(self, value: str) -> None:
        self._check_not_discarded()
        domain_event = Credential.UsernameChanged(
            aggregate_id=self._id.value,
            old_value=self._username,
            new_value=value,
        )
        self._username = value
        self.register_domain_event(domain_event=domain_event)

    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, value: str) -> None:
        self._check_not_discarded()
        domain_event = Credential.PasswordChanged(
            aggregate_id=self._id.value,
            old_value=self._password,
            new_value=value,
        )
        self._password = value
        self.register_domain_event(domain_event=domain_event)

    @property
    def local_ip(self) -> str:
        return self._local_ip

    @local_ip.setter
    def local_ip(self, value: str) -> None:
        self._check_not_discarded()
        domain_event = Credential.LocalIpChanged(
            aggregate_id=self._id.value,
            old_value=self._local_ip,
            new_value=value,
        )
        self._local_ip = value
        self.register_domain_event(domain_event=domain_event)

    @property
    def local_port(self) -> int:
        return self._local_port

    @local_port.setter
    def local_port(self, value: int) -> None:
        self._check_not_discarded()
        domain_event = Credential.LocalPortChanged(
            aggregate_id=self._id.value,
            old_value=self._local_port,
            new_value=value,
        )
        self._local_port = value
        self.register_domain_event(domain_event=domain_event)

    def __repr__(self) -> str:
        return (
            "{d}{c}(id={id!r}, server_id={server_id!r}, connection_type={connection_type!r}, "
            "username={username!r}, password={password!r}, local_ip={local_ip!r}, "
            "local_port={local_port!r}, public_ip={public_ip!r}, public_port={public_port!r}, "
            "discarded={discarded!r})"
        ).format(
            d="*Discarded* " if self._discarded else "",
            c=self.__class__.__name__,
            id=self._id.value,
            server_id=self._server_id.value,
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
        return {
            "id": self._id.value,
            "server_id": self._server_id.value,
            "connection_type": self._connection_type,
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
            id=EntityId.from_string(value=data.get("id")),
            server_id=EntityId.from_string(value=data.get("server_id")),
            connection_type=data.get("connection_type"),
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
        credential = cls(
            id=EntityId.generate(),
            username=username,
            password=password,
            local_ip=local_ip,
            local_port=local_port,
            public_ip=public_ip,
            public_port=public_port,
            discarded=False,
        )
        domain_event = Credential.Created(aggregate_id=credential.id)
        credential.register_domain_event(domain_event=domain_event)
        return credential

    def update(
        self,
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
        if not self.username == username:
            self.username = username
        if not self.password == password:
            self.password = password
        if not self.local_ip == local_ip:
            self.local_ip = local_ip
        if not self.local_port == local_port:
            self.local_port = local_port
        if not self.public_ip == public_ip:
            self.public_ip = public_ip
        if not self.public_port == public_port:
            self.public_port = public_port
        return self

    def discard(self) -> None:
        """
        Important:
            This method is only used to discard an credential.
            When discarding an credential, the discarded attribute is set to True
            and a domain event is registered.
        """
        domain_event = Credential.Discarded(aggregate_id=self._id)
        self._discarded = True
        self.register_domain_event(domain_event=domain_event)
