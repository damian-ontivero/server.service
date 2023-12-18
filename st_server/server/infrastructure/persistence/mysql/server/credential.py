"""Credential database model."""

import sqlalchemy as sa
from sqlalchemy.orm import registry

from st_server.server.domain.server.credential import Credential
from st_server.server.infrastructure.persistence.mysql import db
from st_server.server.infrastructure.persistence.mysql.server.connection_type import (
    ConnectionTypeDbType,
)
from st_server.shared.infrastructure.persistence.mysql.entity_id import (
    EntityIdDbType,
)

mapper_registry = registry()


class CredentialDbModel(db.Base):
    """Credential database model."""

    __tablename__ = "credential"
    __table_args__ = (sa.PrimaryKeyConstraint("id"),)

    id = sa.Column(EntityIdDbType)
    server_id = sa.Column(
        EntityIdDbType, sa.ForeignKey("server.id"), nullable=False
    )
    connection_type = sa.Column(ConnectionTypeDbType, nullable=False)
    local_ip = sa.Column(sa.String(255), nullable=True)
    local_port = sa.Column(sa.String(255), nullable=True)
    public_ip = sa.Column(sa.String(255), nullable=True)
    public_port = sa.Column(sa.String(255), nullable=True)
    username = sa.Column(sa.String(255), nullable=False)
    password = sa.Column(sa.String(255), nullable=False)
    discarded = sa.Column(sa.Boolean, nullable=False)


mapper_registry.map_imperatively(
    Credential,
    CredentialDbModel.__table__,
    properties={
        "_id": CredentialDbModel.id,
        "_server_id": CredentialDbModel.server_id,
        "_connection_type": CredentialDbModel.connection_type,
        "_local_ip": CredentialDbModel.local_ip,
        "_local_port": CredentialDbModel.local_port,
        "_public_ip": CredentialDbModel.public_ip,
        "_public_port": CredentialDbModel.public_port,
        "_username": CredentialDbModel.username,
        "_password": CredentialDbModel.password,
        "_discarded": CredentialDbModel.discarded,
    },
)
