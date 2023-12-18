from st_server.shared.domain.entity_id import EntityId


class ServerApplication:
    """Value object that represents the association between a Server and an Application."""

    __slots__ = ("_server_id", "_application_id", "_install_dir", "_log_dir")

    @classmethod
    def from_data(cls, data: dict) -> "ServerApplication":
        """Named constructor to create the value object from a dictionary."""
        server_id = EntityId.from_text(data.get("server_id"))
        application_id = EntityId.from_text(data.get("application_id"))
        install_dir = data.get("install_dir")
        log_dir = data.get("log_dir")
        return cls(server_id, application_id, install_dir, log_dir)

    def __new__(
        cls,
        server_id: EntityId,
        application_id: EntityId,
        install_dir: str,
        log_dir: str,
    ) -> "ServerApplication":
        """Creates a new instance of the value object."""
        if not isinstance(server_id, EntityId):
            raise TypeError("Server id must be an EntityId")
        if not isinstance(application_id, EntityId):
            raise TypeError("Application id must be an EntityId")
        if not isinstance(install_dir, str):
            raise TypeError("Install dir must be a string")
        if not isinstance(log_dir, str):
            raise TypeError("Log dir must be a string")
        if not len(install_dir) > 0:
            raise ValueError("Install dir cannot be empty")
        if not len(log_dir) > 0:
            raise ValueError("Log dir cannot be empty")
        self = object.__new__(cls)
        self._server_id = server_id
        self._application_id = application_id
        self._install_dir = install_dir
        self._log_dir = log_dir
        return self

    def __eq__(self, other: object) -> bool:
        """Checks if two value objects are equal."""
        if isinstance(other, ServerApplication):
            return (
                self._server_id == other._server_id
                and self._application_id == other._application_id
                and self._install_dir == other._install_dir
                and self._log_dir == other._log_dir
            )
        return NotImplemented

    def __ne__(self, other: object) -> bool:
        """Checks if two value objects are not equal."""
        return not self.__eq__(other)

    def __hash__(self) -> int:
        """Returns the hash of the value object."""
        return hash(
            (
                self._server_id,
                self._application_id,
                self._install_dir,
                self._log_dir,
            )
        )

    def __repr__(self) -> str:
        """Returns the string representation of the value object."""
        return (
            f"{self.__class__.__name__}(server_id={self._server_id!r}, "
            f"application_id={self._application_id!r}, "
            f"install_dir={self._install_dir!r}, log_dir={self._log_dir!r})"
        )

    @property
    def server_id(self) -> EntityId:
        """Returns the Server id."""
        return self._server_id

    @property
    def application_id(self) -> EntityId:
        """Returns the Application id."""
        return self._application_id

    @property
    def install_dir(self) -> str:
        """Returns the install directory."""
        return self._install_dir

    @property
    def log_dir(self) -> str:
        """Returns the log directory."""
        return self._log_dir
