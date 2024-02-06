from fastapi import status
from jwt.exceptions import ExpiredSignatureError

from st_server.shared.application.exception import (
    AlreadyExists,
    AuthenticationError,
    NotFound,
)
from st_server.shared.application.validator.validate_filter import FilterError
from st_server.shared.application.validator.validate_pagination import (
    PaginationError,
)
from st_server.shared.application.validator.validate_sort import SortError

EXCEPTION_TO_HTTP_STATUS_CODE = {
    Exception: status.HTTP_500_INTERNAL_SERVER_ERROR,
    AuthenticationError: status.HTTP_403_FORBIDDEN,
    ExpiredSignatureError: status.HTTP_403_FORBIDDEN,
    PermissionError: status.HTTP_403_FORBIDDEN,
    PaginationError: status.HTTP_400_BAD_REQUEST,
    SortError: status.HTTP_400_BAD_REQUEST,
    FilterError: status.HTTP_400_BAD_REQUEST,
    NotFound: status.HTTP_404_NOT_FOUND,
    AlreadyExists: status.HTTP_422_UNPROCESSABLE_ENTITY,
    ValueError: status.HTTP_400_BAD_REQUEST,
    TypeError: status.HTTP_400_BAD_REQUEST,
}
