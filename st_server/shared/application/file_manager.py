"""Abstract base class for file managers."""

from abc import ABCMeta, abstractmethod


class FileManager(metaclass=ABCMeta):
    """Abstract base class for file managers."""

    @abstractmethod
    def save(self, file_path: str) -> None:
        """Save the file."""
        raise NotImplementedError

    @abstractmethod
    def delete(self, file_path: str) -> None:
        """Delete the file."""
        raise NotImplementedError
