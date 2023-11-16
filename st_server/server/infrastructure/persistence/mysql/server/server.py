"""Server database model."""

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from st_server.server.domain.server.server import Server
from st_server.server.infrastructure.persistence.mysql import db
from st_server.server.infrastructure.persistence.mysql.server.credential import (
    CredentialDbModel,
)
from st_server.server.infrastructure.persistence.mysql.server.server_application import (
    ServerApplicationDbModel,
)


class ServerDbModel(db.Base):
    """Server database model."""

    __tablename__ = "server"

    id = sa.Column(sa.String(32), primary_key=True)
    name = sa.Column(sa.String(255), nullable=False)
    cpu = sa.Column(sa.String(255), nullable=True)
    ram = sa.Column(sa.String(255), nullable=True)
    hdd = sa.Column(sa.String(255), nullable=True)
    environment = sa.Column(sa.String(255), nullable=False)
    operating_system = sa.Column(sa.JSON, nullable=False)
    status = sa.Column(sa.String(255), nullable=True)
    discarded = sa.Column(sa.Boolean, nullable=False)

    credentials = relationship(
        "CredentialDbModel", lazy="subquery", cascade="all, delete-orphan"
    )
    applications = relationship("ServerApplicationDbModel", lazy="subquery")

    @classmethod
    def from_entity(cls, entity: Server) -> "ServerDbModel":
        """Named constructor to create a model from an entity."""
        return cls(
            id=entity.id.value,
            name=entity.name,
            cpu=entity.cpu,
            ram=entity.ram,
            hdd=entity.hdd,
            environment=entity.environment.value,
            operating_system=entity.operating_system.__dict__,
            credentials=[
                CredentialDbModel(
                    id=credential.id.value,
                    connection_type=credential.connection_type.value,
                    username=credential.username,
                    password=credential.password,
                    local_ip=credential.local_ip,
                    local_port=credential.local_port,
                    public_ip=credential.public_ip,
                    public_port=credential.public_port,
                    discarded=credential.discarded,
                )
                for credential in entity.credentials
            ],
            applications=[
                ServerApplicationDbModel(
                    server_id=entity.id.value,
                    application_id=application.id.value,
                    install_dir=application.install_dir,
                    log_dir=application.log_dir,
                )
                for application in entity.applications
            ],
            status=entity.status.value,
            discarded=entity.discarded,
        )

    def to_dict(self) -> dict:
        """Returns a dictiionary representation of the model."""
        return {
            "id": self.id,
            "name": self.name,
            "cpu": self.cpu,
            "ram": self.ram,
            "hdd": self.hdd,
            "environment": self.environment,
            "operating_system": self.operating_system,
            "credentials": [
                credential.to_dict() for credential in self.credentials
            ],
            "applications": [
                application.to_dict() for application in self.applications
            ],
            "status": self.status,
            "discarded": self.discarded,
        }

    def update(self, entity: Server) -> None:
        """Updates the model from an entity."""
        self.name = entity.name
        self.cpu = entity.cpu
        self.ram = entity.ram
        self.hdd = entity.hdd
        self.environment = entity.environment.value
        self.operating_system = entity.operating_system.__dict__
        self.credentials = [
            CredentialDbModel(
                id=credential.id.value,
                connection_type=credential.connection_type.value,
                username=credential.username,
                password=credential.password,
                local_ip=credential.local_ip,
                local_port=credential.local_port,
                public_ip=credential.public_ip,
                public_port=credential.public_port,
                discarded=credential.discarded,
            )
            for credential in entity.credentials
        ]
        self.applications = [
            ServerApplicationDbModel(
                server_id=entity.id.value,
                application_id=application.application_id,
                install_dir=application.install_dir,
                log_dir=application.log_dir,
            )
            for application in entity.applications
        ]
        self.status = entity.status.value
        self.discarded = entity.discarded
