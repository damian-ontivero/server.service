from dataclasses import asdict, dataclass


@dataclass
class Command:
    """
    Base class for commands.

    This class serves as the base for all command classes used within the application.
    """

    def to_dict(self) -> dict[str, any]:
        """Returns the dictionary representation of the command."""
        return asdict(self)
