"""File helper functions."""

import configparser
import os


def save(file: bytes, filename: str) -> str:
    """Saves the file and returns the file path.

    Args:
        file (`bytes`): File to save.
        filename (`str`): File name.

    Returns:
        `str`: File path.
    """
    config = configparser.ConfigParser()
    config.read("st_server/config.ini")

    base_path = config.get("storage", "path")
    filepath = os.path.join(base_path, filename)

    with open(filepath, "wb") as f:
        f.write(file)

    return filepath


def delete(filepath: str) -> None:
    """Deletes the file.

    Args:
        filepath (`str`): File path.
    """
    os.remove(filepath)
