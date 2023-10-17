"""Value object that represents the Operating System of the Server."""


class OperatingSystem:
    """Value object that represents the Operating System of the Server."""

    __slots__ = ("_name", "_version", "_architecture")

    def __new__(
        cls, name: str, version: str, architecture: str
    ) -> "OperatingSystem":
        """Creates a new instance of Operating System."""
        if not isinstance(name, str):
            raise TypeError("Operating system name must be a string")
        if not len(name) > 0:
            raise ValueError("Operating system name cannot be empty")
        if not isinstance(version, str):
            raise TypeError("Operating system version must be a string")
        if not len(version) > 0:
            raise ValueError("Operating system version cannot be empty")
        if not isinstance(architecture, str):
            raise TypeError("Operating system architecture must be a string")
        if not len(architecture) > 0:
            raise ValueError("Operating system architecture cannot be empty")
        self = object.__new__(cls)
        self._name = name
        self._version = version
        self._architecture = architecture
        return self

    @property
    def name(self) -> str:
        """Returns the name of the Operating System."""
        return self._name

    @property
    def version(self) -> str:
        """Returns the version of the Operating System."""
        return self._version

    @property
    def architecture(self) -> str:
        """Returns the architecture of the Operating System."""
        return self._architecture

    @property
    def __dict__(self) -> dict:
        """Returns the Operating System as a dictionary."""
        return {
            "name": self.name,
            "version": self.version,
            "architecture": self.architecture,
        }

    @classmethod
    def from_data(cls, data: dict) -> "OperatingSystem":
        """Named constructor to create an Operating System from a dictionary."""
        return cls(
            name=data.get("name"),
            version=data.get("version"),
            architecture=data.get("architecture"),
        )

    def __eq__(self, other: object) -> bool:
        """Compares if two Operating System are equal."""
        if isinstance(other, OperatingSystem):
            return (
                self.name == other.name
                and self.version == other.version
                and self.architecture == other.architecture
            )
        return NotImplemented

    def __ne__(self, other: object) -> bool:
        """Compares if two Operating System are not equal."""
        return not self.__eq__(other)

    def __hash__(self) -> int:
        """Returns the hash of the Operating System."""
        return hash((self._name, self._version, self._architecture))

    def __repr__(self) -> str:
        """Returns the representation of the Operating System."""
        return (
            "{c}(name={name!r}, version={version!r}, "
            "architecture={architecture!r})"
        ).format(
            c=self.__class__.__name__,
            name=self.name,
            version=self.version,
            architecture=self.architecture,
        )
