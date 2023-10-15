"""Server database model."""

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from st_server.server.infrastructure.mysql import db
from st_server.server.infrastructure.mysql.model.credential import (
    CredentialDbModel,
)
from st_server.server.infrastructure.mysql.model.server_application import (
    ServerApplicationDbModel,
)
from st_server.server.domain.entity.server import Server


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
        "CredentialDbModel", lazy="joined", cascade="all, delete-orphan"
    )
    applications = relationship("ServerApplicationDbModel", lazy="joined")

    def update(self, entity: Server):
        """Updates the server model from a server entity."""
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
                application_id=application.id.value,
                install_dir=application.install_dir,
                log_dir=application.log_dir,
            )
            for application in entity.applications
        ]
        self.status = entity.status.value
        self.discarded = entity.discarded
