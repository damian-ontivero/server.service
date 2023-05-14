"""Credential database model."""

import sqlalchemy as sa

from st_server.infrastructure.mysql import db


class CredentialDbModel(db.Base):
    """Credential database model."""

    __tablename__ = "credential"

    id = sa.Column(
        sa.String(32), primary_key=True, unique=True, nullable=False
    )
    server_id = sa.Column(sa.ForeignKey("server.id"), nullable=False)
    connection_type = sa.Column(sa.String(255), nullable=False)
    local_ip = sa.Column(sa.String(255), nullable=True)
    local_port = sa.Column(sa.String(255), nullable=True)
    public_ip = sa.Column(sa.String(255), nullable=True)
    public_port = sa.Column(sa.String(255), nullable=True)
    username = sa.Column(sa.String(255), nullable=False)
    password = sa.Column(sa.String(255), nullable=False)
    discarded = sa.Column(sa.Boolean, nullable=False, default=False)

    def __repr__(self) -> str:
        """Returns the string representation of the object.

        Returns:
            `str`: String representation of the object.
        """
        return (
            f"CredentialDbModel(id={self.id}, "
            f"server_id={self.server_id}, "
            f"connection_type={self.connection_type}, "
            f"local_ip={self.local_ip}, local_port={self.local_port}, "
            f"public_ip={self.public_ip}, public_port={self.public_port}, "
            f"username={self.username}, password={self.password}, "
            f"discarded={self.discarded})"
        )

    def to_dict(self, exclude: list[str] = None) -> dict:
        """Returns a dictionary representation of the object.

        Args:
            exclude (`list[str]`, optional): List of attributes to exclude.

        Returns:
            `dict`: Dictionary representation of the object.
        """
        data = {
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

        if exclude:
            for attr in exclude:
                del data[attr]

        return data

    def from_dict(data: dict) -> "CredentialDbModel":
        """Returns an instance of the class based on the provided dictionary.

        Args:
            data (`dict`): Dictionary representation of the object.

        Returns:
            `CredentialDbModel`: Instance of the class.
        """
        return CredentialDbModel(
            id=data.get("id"),
            server_id=data.get("server_id"),
            connection_type=data.get("connection_type"),
            local_ip=data.get("local_ip"),
            local_port=data.get("local_port"),
            public_ip=data.get("public_ip"),
            public_port=data.get("public_port"),
            username=data.get("username"),
            password=data.get("password"),
            discarded=data.get("discarded"),
        )
