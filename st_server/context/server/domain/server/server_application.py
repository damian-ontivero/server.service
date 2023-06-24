"""ServerApplication relationship."""

from st_server.context.server.domain.application.application import Application
from st_server.shared.core.aggregate_root import AggregateRoot
from st_server.shared.core.domain_event import DomainEvent
from st_server.shared.core.entity_id import EntityId


class ServerApplication:
    """ServerApplication relationship."""

    def __init__(
        self,
        server_id: EntityId | None = None,
        application_id: EntityId | None = None,
        install_dir: str | None = None,
        log_dir: str | None = None,
        application: Application | None = None,
    ) -> None:
        """
        Important:
            Do not use directly to create a new ServerApplication.
        """
        self._server_id = server_id
        self._application_id = application_id
        self._install_dir = install_dir
        self._log_dir = log_dir
        self._application = application

    @property
    def server_id(self) -> str:
        return self._server_id

    @server_id.setter
    def server_id(self, server_id: EntityId) -> None:
        self._server_id = server_id

    @property
    def application_id(self) -> EntityId:
        return self._application_id

    @application_id.setter
    def application_id(self, application_id: EntityId) -> None:
        self._application_id = application_id

    @property
    def install_dir(self) -> str:
        return self._install_dir

    @install_dir.setter
    def install_dir(self, install_dir: str) -> None:
        self._install_dir = install_dir

    @property
    def log_dir(self) -> str:
        return self._log_dir

    @log_dir.setter
    def log_dir(self, log_dir: str) -> None:
        self._log_dir = log_dir

    @property
    def application(self) -> Application:
        return self._application

    @application.setter
    def application(self, application: Application) -> None:
        self._application = application

    def __repr__(self) -> str:
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

    def to_dict(self) -> dict:
        return {
            "server_id": self._server_id.value,
            "application_id": self._application_id.value,
            "install_dir": self._install_dir,
            "log_dir": self._log_dir,
            "application": self._application.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ServerApplication":
        for k, v in data.items():
            if k == "application":
                data[k] = Application.from_dict(data=v)
        return cls(
            server_id=EntityId.from_string(value=data.get("server_id")),
            application_id=EntityId.from_string(
                value=data.get("application_id")
            ),
            install_dir=data.get("install_dir"),
            log_dir=data.get("log_dir"),
            application=data.get("application"),
        )
