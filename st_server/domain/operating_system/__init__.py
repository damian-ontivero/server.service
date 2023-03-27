"""This is the Operating System aggregate entity package.

The aggregate root for this Operating System aggregate is the Operating System entity.
"""

from .operating_system import (
    OperatingSystem,
    OperatingSystemCreate,
    OperatingSystemFull,
    OperatingSystemUpdate,
)
from .operating_system_exception import (
    OperatingSystemAlreadyExists,
    OperatingSystemNameAlreadyExists,
    OperatingSystemNotFound,
)
from .operating_system_repository import OperatingSystemAbstractRepository
from .operating_system_service import OperatingSystemAbstractService

__all__ = [
    "OperatingSystem",
    "OperatingSystemCreate",
    "OperatingSystemFull",
    "OperatingSystemUpdate",
    "OperatingSystemAlreadyExists",
    "OperatingSystemNameAlreadyExists",
    "OperatingSystemNotFound",
    "OperatingSystemAbstractRepository",
    "OperatingSystemAbstractService",
]
