"""Server router."""

import json

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import ExpiredSignatureError

from st_server.server.application.command.server.add.add_server_command import (
    AddServerCommand,
)
from st_server.server.application.command.server.add.add_server_command_handler import (
    AddServerCommandHandler,
)
from st_server.server.application.command.server.delete.delete_server_command import (
    DeleteServerCommand,
)
from st_server.server.application.command.server.delete.delete_server_command_handler import (
    DeleteServerCommandHandler,
)
from st_server.server.application.command.server.update.update_server_command import (
    UpdateServerCommand,
)
from st_server.server.application.command.server.update.update_server_command_handler import (
    UpdateServerCommandHandler,
)
from st_server.server.application.dto.server.server import ServerReadDto
from st_server.shared.application.exception.exception import (
    AlreadyExists,
    AuthenticationError,
    FilterError,
    NotFound,
    PaginationError,
    SortError,
)
from st_server.shared.application.response.query_response import QueryResponse

router = APIRouter()
auth_scheme = HTTPBearer()


@router.get("", response_model=QueryResponse)
def get_all(
    limit: int = Query(default=25),
    offset: int = Query(default=0),
    filter: str = Query(default="{}"),
    and_filter: str | None = Query(default="[]"),
    or_filter: str | None = Query(default="[]"),
    sort: str | None = Query(default="[]"),
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
    request: Request = None,
):
    """Route to get all servers."""
    try:
        servers = query.find_many(
            limit=limit,
            offset=offset,
            filter=json.loads(filter),
            and_filter=json.loads(and_filter),
            or_filter=json.loads(or_filter),
            sort=json.loads(sort),
            access_token=authorization.credentials,
        )
        if servers.total == 0:
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
        return JSONResponse(
            content=jsonable_encoder(obj=servers),
            status_code=status.HTTP_200_OK,
        )
    except ExpiredSignatureError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=str(e)
        )
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=str(e)
        )
    except PaginationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
    except SortError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
    except FilterError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


@router.get("/{id}", response_model=ServerReadDto)
def get(
    id: str,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    """Route to get a Server by id."""
    try:
        server = query.find_one(id=id, access_token=authorization.credentials)
        return JSONResponse(content=jsonable_encoder(obj=server))
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=str(e)
        )
    except NotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )


@router.post("", response_model=ServerReadDto)
def create(
    command: AddServerCommand,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    """Route to create a Server."""
    try:
        server = AddServerCommandHandler(command)
        return JSONResponse(
            content=jsonable_encoder(obj=server),
            status_code=status.HTTP_201_CREATED,
        )
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=str(e)
        )
    except AlreadyExists as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
    except TypeError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


@router.put("/{id}", response_model=ServerReadDto)
def update(
    id: str,
    command: UpdateServerCommand,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    """Route to update a Server."""
    try:
        server = UpdateServerCommandHandler(
            repository=repository, message_bus=message_bus
        ).handle(command)
        return JSONResponse(
            content=jsonable_encoder(obj=server),
            status_code=status.HTTP_200_OK,
        )
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=str(e)
        )
    except NotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    except AlreadyExists as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
    except TypeError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


@router.delete("/{id}")
def delete(
    id: str,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    """Route to discard a Server."""
    try:
        command = DeleteServerCommand(id=id)
        DeleteServerCommandHandler(
            repository=repository, message_bus=message_bus
        ).handle(command)
        return JSONResponse(
            content=jsonable_encoder(
                obj={"message": "The Server has been deleted"}
            ),
            status_code=status.HTTP_200_OK,
        )
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=str(e)
        )
    except NotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
