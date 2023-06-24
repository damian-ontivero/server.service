"""Domain exceptions."""


class NotFound(Exception):
    def __init__(self, message: str | None = None) -> None:
        if message is None:
            message = "Entity not found"
        super().__init__(message)
        self._message = message

    def __str__(self) -> str:
        return self._message


class AlreadyExists(Exception):
    def __init__(self, message: str | None = None) -> None:
        if message is None:
            message = "Entity already exists"
        super().__init__(message)
        self._message = message

    def __str__(self) -> str:
        return self._message


class AuthenticationError(Exception):
    def __init__(self, message: str | None = None) -> None:
        if message is None:
            message = "Authentication failed"
        super().__init__(message)
        self._message = message

    def __str__(self) -> str:
        return self._message


class PasswordError(Exception):
    def __init__(self, message: str | None = None) -> None:
        if message is None:
            message = "Password is incorrect"
        super().__init__(message)
        self._message = message

    def __str__(self) -> str:
        return self._message


class PaginationError(Exception):
    def __init__(self, message: str | None = None) -> None:
        if message is None:
            message = "Pagination failed"
        super().__init__(message)
        self._message = message

    def __str__(self) -> str:
        return self._message


class FilterError(Exception):
    def __init__(self, message: str | None = None) -> None:
        if message is None:
            message = "Incorrect filter format"
        super().__init__(message)
        self._message = message

    def __str__(self) -> str:
        return self._message


class SortError(Exception):
    def __init__(self, message: str | None = None) -> None:
        if message is None:
            message = "Incorrect sort format'"
        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        return self.message
