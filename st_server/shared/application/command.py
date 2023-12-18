from dataclasses import asdict, dataclass
from typing import Dict


@dataclass
class Command:
    """
    Base class for commands.

    This class serves as the base for all command classes used within the application.
    """

    def to_dict(self) -> Dict[str, any]:
        """Returns the dictionary representation of the command."""
        return asdict(self)
