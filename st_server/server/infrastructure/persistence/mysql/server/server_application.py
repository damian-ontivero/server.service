from sqlalchemy import Column, ForeignKey, String

from st_server.server.infrastructure.persistence.mysql import db


class ServerApplicationDbModel(db.Base):
    """ServerApplication database model."""

    __tablename__ = "server_application"

    server_id = Column(ForeignKey("server.id"), primary_key=True)
    application_id = Column(ForeignKey("application.id"), primary_key=True)
    install_dir = Column(String(255))
    log_dir = Column(String(255))
