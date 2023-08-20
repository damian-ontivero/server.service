"""Value object that represents the operating system of the Server."""


class OperatingSystem:
    """Value object that represents the operating system of the Server."""

    __slots__ = ("_name", "_version", "_architecture")

    def __new__(
        cls, name: str, version: str, architecture: str
    ) -> "OperatingSystem":
        """Creates a new instance of operating system."""
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
        self.__setattr("_name", name)
        self.__setattr("_version", version)
        self.__setattr("_architecture", architecture)
        return self

    @classmethod
    def from_dict(cls, value: dict) -> "OperatingSystem":
        """Named constructor for creating a operating system from a dictionary."""
        return cls(
            name=value.get("name"),
            version=value.get("version"),
            architecture=value.get("architecture"),
        )

    @property
    def name(self) -> str:
        """Returns the name of the operating system."""
        return self._name

    @property
    def version(self) -> str:
        """Returns the version of the operating system."""
        return self._version

    @property
    def architecture(self) -> str:
        """Returns the architecture of the operating system."""
        return self._architecture

    @property
    def __dict__(self) -> dict:
        """Returns the dictionary representation of the operating system."""
        return {
            "name": self.name,
            "version": self.version,
            "architecture": self.architecture,
        }

    def __setattr__(self, name: str, value: object) -> None:
        """Prevents setting attributes."""
        raise AttributeError("Operating system objects are immutable")

    def __delattr__(self, name: str) -> None:
        """Prevents deleting attributes."""
        raise AttributeError("Operating system objects are immutable")

    def __eq__(self, other: object) -> bool:
        """Compares if two operating system are equal."""
        if isinstance(other, OperatingSystem):
            return (
                self.name == other.name
                and self.version == other.version
                and self.architecture == other.architecture
            )
        return NotImplemented

    def __ne__(self, other: object) -> bool:
        """Compares if two operating system are not equal."""
        return not self.__eq__(other)

    def __hash__(self) -> int:
        """Returns the hash of the operating system."""
        return hash((self.name, self.version, self.architecture))

    def __repr__(self) -> str:
        """Returns the representation of the operating system."""
        return (
            "{c}(name={name!r}, version={version!r}, "
            "architecture={architecture!r})"
        ).format(
            c=self.__class__.__name__,
            name=self.name,
            version=self.version,
            architecture=self.architecture,
        )

    def __setattr(self, name: str, value: object) -> None:
        """Private method for setting attributes."""
        object.__setattr__(self, name, value)
