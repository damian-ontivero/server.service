from abc import ABCMeta, abstractmethod


class FileManager(metaclass=ABCMeta):
    """Abstract base class for file managers.

    This class represents a blueprint for managing files within the application.
    """

    @abstractmethod
    def save(self, file_path: str) -> None:
        """Saves the file."""
        raise NotImplementedError

    @abstractmethod
    def delete(self, file_path: str) -> None:
        """Deletes the file if it exists."""
        raise NotImplementedError
