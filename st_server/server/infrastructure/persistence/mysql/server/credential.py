"""Credential database model."""

import sqlalchemy as sa

from st_server.server.domain.server.credential import Credential
from st_server.server.infrastructure.persistence.mysql import db
from st_server.server.infrastructure.persistence.mysql.server.connection_type import (
    ConnectionTypeDbType,
)
from st_server.shared.infrastructure.persistence.mysql.entity_id import (
    EntityIdDbType,
)


class CredentialDbModel(db.Base):
    """Credential database model."""

    __tablename__ = "credential"
    __table_args__ = (sa.PrimaryKeyConstraint("id"),)

    id = sa.Column(EntityIdDbType)
    server_id = sa.Column(EntityIdDbType, sa.ForeignKey("server.id"))
    connection_type = sa.Column(ConnectionTypeDbType)
    local_ip = sa.Column(sa.String(255))
    local_port = sa.Column(sa.String(255))
    public_ip = sa.Column(sa.String(255))
    public_port = sa.Column(sa.String(255))
    username = sa.Column(sa.String(255))
    password = sa.Column(sa.String(255))
    discarded = sa.Column(sa.Boolean)


db.Base.registry.map_imperatively(
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
