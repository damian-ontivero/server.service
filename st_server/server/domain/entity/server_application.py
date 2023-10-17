"""Server Application relationship."""

from st_server.server.domain.entity.application import Application
from st_server.shared.domain.value_object.entity_id import EntityId


class ServerApplication:
    """Server Application relationship."""

    def __init__(
        self,
        server_id: EntityId | None = None,
        application_id: EntityId | None = None,
        install_dir: str | None = None,
        log_dir: str | None = None,
        application: Application | None = None,
    ) -> None:
        """Initialize the Server Application.

        Important:
            Do not use directly to create a new Server Application.
        """
        self._server_id = server_id
        self._application_id = application_id
        self._install_dir = install_dir
        self._log_dir = log_dir
        self._application = application

    @property
    def server_id(self) -> EntityId:
        """Returns the Server id of the Server Application."""
        return self._server_id

    @server_id.setter
    def server_id(self, server_id: EntityId) -> None:
        """Sets the Server id of the Server Application."""
        self._server_id = server_id

    @property
    def application_id(self) -> EntityId:
        """Returns the Application id of the Server Application."""
        return self._application_id

    @application_id.setter
    def application_id(self, application_id: EntityId) -> None:
        """Sets the Application id of the Server Application."""
        self._application_id = application_id

    @property
    def install_dir(self) -> str:
        """Returns the install dir of the Server Application."""
        return self._install_dir

    @install_dir.setter
    def install_dir(self, install_dir: str) -> None:
        """Sets the install dir of the Server Application."""
        self._install_dir = install_dir

    @property
    def log_dir(self) -> str:
        """Returns the log dir of the Server Application."""
        return self._log_dir

    @log_dir.setter
    def log_dir(self, log_dir: str) -> None:
        """Sets the log dir of the Server Application."""
        self._log_dir = log_dir

    @property
    def application(self) -> Application:
        """Returns the Application of the Server Application."""
        return self._application

    @application.setter
    def application(self, application: Application) -> None:
        """Sets the Application of the Server Application."""
        self._application = application

    @classmethod
    def create(
        cls,
        server_id: EntityId,
        application_id: EntityId,
        install_dir: str,
        log_dir: str,
    ) -> "ServerApplication":
        """Named constructor to create a new Server Application."""
        return cls(
            server_id=server_id,
            application_id=application_id,
            install_dir=install_dir,
            log_dir=log_dir,
        )

    def __repr__(self) -> str:
        """Returns the representation of the Server Application."""
        return (
            "{c}(server_id={server_id!r}, application_id={application_id!r}, "
            "install_dir={install_dir!r}, log_dir={log_dir!r}, application={application!r})"
        ).format(
            c=self.__class__.__name__,
            server_id=self._server_id.value,
            application_id=self._application_id.value,
            install_dir=self._install_dir,
            log_dir=self._log_dir,
            application=self._application,
        )
