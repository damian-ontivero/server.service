from sqlalchemy import Boolean, Column, ForeignKey, String

from st_server.server.infrastructure.persistence.mysql import db


class CredentialDbModel(db.Base):
    """Credential database model."""

    __tablename__ = "credential"

    id = Column(String(32), primary_key=True)
    server_id = Column(String(32), ForeignKey("server.id"))
    connection_type = Column(String(255))
    local_ip = Column(String(255))
    local_port = Column(String(255))
    public_ip = Column(String(255))
    public_port = Column(String(255))
    username = Column(String(255))
    password = Column(String(255))
    discarded = Column(Boolean)
