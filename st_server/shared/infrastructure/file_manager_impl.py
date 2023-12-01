"""File manager implementation."""

import os

from st_server.shared.application.file_manager import FileManager


class FileManagerImpl(FileManager):
    """File manager implementation."""

    def save(self, file_path: str) -> None:
        """Save the file."""
        with open(file_path, "w") as file:
            file.write("Hello, world!")

    def delete(self, file_path: str) -> None:
        """Delete the file."""
        os.remove(file_path)
