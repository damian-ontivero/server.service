"""File helper functions."""

import configparser
import os


def save(file: bytes, filename: str) -> str:
    """Saves a file to the storage path."""
    config = configparser.ConfigParser()
    config.read("st_server/config.ini")
    base_path = config.get("storage", "path")
    filepath = os.path.join(base_path, filename)
    with open(filepath, "wb") as f:
        f.write(file)
    return filepath


def delete(filepath: str) -> None:
    """Deletes a file from the storage path."""
    os.remove(filepath)
