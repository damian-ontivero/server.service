"""Application database model."""

import sqlalchemy as sa

from st_server.infrastructure.mysql import db


class ApplicationDbModel(db.Base):
    """Application database model."""

    __tablename__ = "application"

    id = sa.Column(
        sa.String(32), primary_key=True, unique=True, nullable=False
    )
    name = sa.Column(sa.String(255), nullable=False)
    version = sa.Column(sa.String(255), nullable=False)
    architect = sa.Column(sa.String(255), nullable=False)
    discarded = sa.Column(sa.Boolean, nullable=False, default=False)

    def __repr__(self) -> str:
        """Returns the string representation of the object.

        Returns:
            `str`: String representation of the object.
        """
        return (
            f"ApplicationDbModel(id={self.id}, name={self.name}, "
            f"version={self.version}, architect={self.architect}, "
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
            "name": self.name,
            "version": self.version,
            "architect": self.architect,
            "discarded": self.discarded,
        }

        if exclude:
            for attr in exclude:
                del data[attr]

        return data

    def from_dict(data: dict) -> "ApplicationDbModel":
        """Returns an instance of the class based on the provided dictionary.

        Args:
            data (`dict`): Dictionary representation of the object.

        Returns:
            `ApplicationDbModel`: Instance of the class.
        """
        return ApplicationDbModel(
            id=data.get("id"),
            name=data.get("name"),
            version=data.get("version"),
            architect=data.get("architect"),
            discarded=data.get("discarded"),
        )
