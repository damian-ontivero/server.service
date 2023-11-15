"""File helper functions."""

import os


def save(file: bytes, filepath: os.PathLike, overwrite: bool = False) -> None:
    """Saves a file to the storage path."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    if os.path.isfile(filepath) and not overwrite:
        raise FileExistsError
    with open(filepath, "wb") as f:
        f.write(file)


def delete(filepath: str) -> None:
    """Deletes a file from the storage path."""
    if os.path.isfile(filepath):
        os.remove(filepath)
