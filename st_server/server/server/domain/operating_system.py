class OperatingSystem:
    __slots__ = ("_name", "_version", "_architecture")

    @classmethod
    def from_data(cls, data: dict) -> "OperatingSystem":
        return cls(
            name=data.get("name"),
            version=data.get("version"),
            architecture=data.get("architecture"),
        )

    def __new__(
        cls, name: str, version: str, architecture: str
    ) -> "OperatingSystem":
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

    def __eq__(self, other: object) -> bool:
        if isinstance(other, OperatingSystem):
            return (
                self.name == other.name
                and self.version == other.version
                and self.architecture == other.architecture
            )
        return NotImplemented

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash((self.name, self.version, self.architecture))

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(name={self._name!r}, "
            f"version={self._version!r}, architecture={self._architecture!r})"
        )

    @property
    def name(self) -> str:
        return self._name

    @property
    def version(self) -> str:
        return self._version

    @property
    def architecture(self) -> str:
        return self._architecture

    @property
    def __dict__(self) -> dict:
        return {
            "name": self._name,
            "version": self._version,
            "architecture": self._architecture,
        }
