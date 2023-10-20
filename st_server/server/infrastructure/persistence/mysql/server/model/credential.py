"""Credential database model."""

import sqlalchemy as sa

from st_server.server.domain.entity.server.credential import Credential
from st_server.server.infrastructure.persistence.mysql import session


class CredentialDbModel(session.Base):
    """Credential database model."""

    __tablename__ = "credential"

    id = sa.Column(sa.String(32), primary_key=True)
    server_id = sa.Column(sa.ForeignKey("server.id"), nullable=False)
    connection_type = sa.Column(sa.String(255), nullable=False)
    local_ip = sa.Column(sa.String(255), nullable=True)
    local_port = sa.Column(sa.String(255), nullable=True)
    public_ip = sa.Column(sa.String(255), nullable=True)
    public_port = sa.Column(sa.String(255), nullable=True)
    username = sa.Column(sa.String(255), nullable=False)
    password = sa.Column(sa.String(255), nullable=False)
    discarded = sa.Column(sa.Boolean, nullable=False)

    def to_dict(self) -> dict:
        """Returns a dictiionary representation of the model."""
        return {
            "id": self.id,
            "server_id": self.server_id,
            "connection_type": self.connection_type,
            "local_ip": self.local_ip,
            "local_port": self.local_port,
            "public_ip": self.public_ip,
            "public_port": self.public_port,
            "username": self.username,
            "password": self.password,
            "discarded": self.discarded,
        }

    def update(self, entity: Credential) -> None:
        """Updates the model from an entity."""
        self.connection_type = entity.connection_type.value
        self.local_ip = entity.local_ip
        self.local_port = entity.local_port
        self.public_ip = entity.public_ip
        self.public_port = entity.public_port
        self.username = entity.username
        self.password = entity.password
        self.discarded = entity.discarded
