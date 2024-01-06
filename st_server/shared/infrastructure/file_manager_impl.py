import os

from st_server.shared.application.file_manager import FileManager


class FileManagerImpl(FileManager):
    def save(self, file_path: str, content: str) -> None:
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))
        with open(file_path, "w") as f:
            f.write(content)

    def delete(self, file_path: str) -> None:
        if os.path.exists(file_path):
            os.remove(file_path)
        else:
            raise FileNotFoundError(f"File {file_path} not found")
