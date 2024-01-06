from sqlalchemy import Boolean, Column, String

from st_server.server.infrastructure.persistence.mysql import db


class ApplicationDbModel(db.Base):
    __tablename__ = "application"

    id = Column(String(32), primary_key=True)
    name = Column(String(255))
    version = Column(String(255))
    architect = Column(String(255))
    discarded = Column(Boolean)
