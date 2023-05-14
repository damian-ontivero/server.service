"""Server application relationship."""

from st_server.domain.aggregate_root import AggregateRoot
from st_server.domain.application.application import Application
from st_server.domain.domain_event import DomainEvent
from st_server.domain.entity_id import EntityId


class ServerApplication:
    """Server application relationship."""

    def __init__(
        self,
        server_id: EntityId | None = None,
        application_id: EntityId | None = None,
        install_dir: str | None = None,
        log_dir: str | None = None,
        application: Application | None = None,
    ) -> None:
        """Constructor of the relationship.

        Args:
            server_id (`EntityId`): Server id of the relationship.
            application_id (`EntityId`): Application id of the relationship.
            install_dir (`str`): Install directory of the relationship.
            log_dir (`str`): Log directory of the relationship.
            application (`Application`): Application of the relationship.
        """
        self._server_id = server_id
        self._application_id = application_id
        self._install_dir = install_dir
        self._log_dir = log_dir
        self._application = application

    @property
    def server_id(self) -> EntityId:
        """Server id getter.

        Returns:
            `EntityId`: Server id of the relationship.
        """
        return self._server_id

    @server_id.setter
    def server_id(self, server_id: EntityId) -> None:
        """Server id setter.

        Args:
            server_id (`EntityId`): Server id of the relationship.
        """
        self._server_id = server_id

    @property
    def application_id(self) -> EntityId:
        """Application id getter.

        Returns:
            `EntityId`: Application id of the relationship.
        """
        return self._application_id

    @application_id.setter
    def application_id(self, application_id: EntityId) -> None:
        """Application id setter.

        Args:
            application_id (`EntityId`): Application id of the relationship.
        """
        self._application_id = application_id

    @property
    def install_dir(self) -> str:
        """Install directory getter.

        Returns:
            `str`: Install directory of the relationship.
        """
        return self._install_dir

    @install_dir.setter
    def install_dir(self, install_dir: str) -> None:
        """Install directory setter.

        Args:
            install_dir (`str`): Install directory of the relationship.
        """
        self._install_dir = install_dir

    @property
    def log_dir(self) -> str:
        """Log directory getter.

        Returns:
            `str`: Log directory of the relationship.
        """
        return self._log_dir

    @log_dir.setter
    def log_dir(self, log_dir: str) -> None:
        """Log directory setter.

        Args:
            log_dir (`str`): Log directory of the relationship.
        """
        self._log_dir = log_dir

    @property
    def application(self) -> Application:
        """Application getter.

        Returns:
            `Application`: Application of the relationship.
        """
        return self._application

    @application.setter
    def application(self, application: Application) -> None:
        """Application setter.

        Args:
            application (`Application`): Application of the relationship.
        """
        self._application = application

    def __repr__(self) -> str:
        """Returns the string representation of the object.

        Returns:
            `str`: String representation of the object.
        """
        return (
            f"ServerApplication(server_id={self._server_id}, "
            f"application_id={self._application_id}, "
            f"install_dir={self._install_dir}, log_dir={self._log_dir}, "
            f"application={self._application})"
        )

    def to_dict(self) -> dict:
        """Returns a dictionary representation of the object.

        Returns:
            `dict`: Dictionary representation of the object.
        """
        return {
            "server_id": self._server_id,
            "application_id": self._application_id,
            "install_dir": self._install_dir,
            "log_dir": self._log_dir,
            "application": self._application.to_dict(),
        }

    @staticmethod
    def from_dict(data: dict) -> "ServerApplication":
        """Returns an instance of the class based on the provided dictionary.

        Args:
            data (`dict`): Dictionary representation of the object.

        Returns:
            `ServerApplication`: Instance of the class.
        """
        for k, v in data.items():
            if k == "application":
                data[k] = Application.from_dict(data=v)

        return ServerApplication(**data)
