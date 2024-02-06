from sqlalchemy import JSON, Boolean, Column, String
from sqlalchemy.orm import relationship

from st_server.shared.infrastructure.persistence.mysql import db


class ServerDbModel(db.Base):
    __tablename__ = "server"

    id = Column(String(32), primary_key=True)
    name = Column(String(255))
    cpu = Column(String(255))
    ram = Column(String(255))
    hdd = Column(String(255))
    environment = Column(String(255))
    operating_system = Column(JSON)
    status = Column(String(255))
    discarded = Column(Boolean)

    credentials = relationship(
        "CredentialDbModel", cascade="all, delete-orphan"
    )
    applications = relationship(
        "ServerApplicationDbModel", cascade="all, delete-orphan"
    )
