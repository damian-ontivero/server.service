from abc import ABCMeta, abstractmethod


class FileManager(metaclass=ABCMeta):
    """
    Abstract base class for file managers.

    This class represents a blueprint for managing files within the application.
    """

    @abstractmethod
    def save(self, file_path: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, file_path: str) -> None:
        raise NotImplementedError
