"""Server router."""

import json

from fastapi import APIRouter, Depends, Query, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from st_server.server.application.server.command.add_server_command import (
    AddServerCommand,
)
from st_server.server.application.server.command.add_server_command_handler import (
    AddServerCommandHandler,
)
from st_server.server.application.server.command.delete_server_command import (
    DeleteServerCommand,
)
from st_server.server.application.server.command.delete_server_command_handler import (
    DeleteServerCommandHandler,
)
from st_server.server.application.server.command.update_server_command import (
    UpdateServerCommand,
)
from st_server.server.application.server.command.update_server_command_handler import (
    UpdateServerCommandHandler,
)
from st_server.server.application.server.dto.server import ServerReadDto
from st_server.server.application.server.query.find_many_query import (
    FindManyServerQuery,
)
from st_server.server.application.server.query.find_many_query_handler import (
    FindManyServerQueryHandler,
)
from st_server.server.application.server.query.find_one_query import (
    FindOneServerQuery,
)
from st_server.server.application.server.query.find_one_query_handler import (
    FindOneServerQueryHandler,
)
from st_server.shared.application.query_response import QueryResponse

router = APIRouter()
auth_scheme = HTTPBearer()


@router.get("", response_model=QueryResponse)
def get_all(
    query: FindManyServerQuery,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    """Route to get all servers."""
    servers = FindManyServerQueryHandler().handle(query)
    if servers.total == 0:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    return JSONResponse(
        content=jsonable_encoder(obj=servers),
        status_code=status.HTTP_200_OK,
    )


@router.get("/{id}", response_model=ServerReadDto)
def get(
    query: FindOneServerQuery,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    """Route to get a Server by id."""
    server = FindOneServerQueryHandler().handle(query)
    return JSONResponse(
        content=jsonable_encoder(obj=server), status_code=status.HTTP_200_OK
    )


@router.post("", response_model=ServerReadDto)
def create(
    command: AddServerCommand,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    """Route to create a Server."""
    AddServerCommandHandler(command)
    return JSONResponse(
        content=jsonable_encoder(obj=command),
        status_code=status.HTTP_201_CREATED,
    )


@router.put("/{id}", response_model=ServerReadDto)
def update(
    command: UpdateServerCommand,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    """Route to update a Server."""
    UpdateServerCommandHandler().handle(command)
    return JSONResponse(
        content=jsonable_encoder(obj=command),
        status_code=status.HTTP_200_OK,
    )


@router.delete("/{id}")
def delete(
    command: DeleteServerCommand,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    """Route to discard a Server."""
    DeleteServerCommandHandler().handle(command)
    return JSONResponse(
        content=jsonable_encoder(
            obj={"message": "The Server has been deleted"}
        ),
        status_code=status.HTTP_200_OK,
    )
