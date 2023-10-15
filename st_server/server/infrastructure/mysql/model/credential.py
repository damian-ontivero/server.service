"""Credential database model."""

import sqlalchemy as sa

from st_server.server.infrastructure.mysql import db
from st_server.server.domain.entity.credential import Credential


class CredentialDbModel(db.Base):
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

    def update(self, entity: Credential) -> None:
        """Updates the credential model from a credential entity."""
        self.connection_type = entity.connection_type.value
        self.local_ip = entity.local_ip
        self.local_port = entity.local_port
        self.public_ip = entity.public_ip
        self.public_port = entity.public_port
        self.username = entity.username
        self.password = entity.password
        self.discarded = entity.discarded
