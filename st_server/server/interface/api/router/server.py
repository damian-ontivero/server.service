"""Server router."""

from fastapi import APIRouter, Depends, Query, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from st_server.server.application.server.command.add_server_command import (
    AddServerCommand,
)
from st_server.server.application.server.command.delete_server_command import (
    DeleteServerCommand,
)
from st_server.server.application.server.command.update_server_command import (
    UpdateServerCommand,
)
from st_server.server.application.server.dto.server import ServerReadDto
from st_server.server.application.server.query.find_many_server_query import (
    FindManyServerQuery,
)
from st_server.server.application.server.query.find_one_server_query import (
    FindOneServerQuery,
)
from st_server.server.interface.controller.server.add_server_controller import (
    AddServerController,
)
from st_server.server.interface.controller.server.delete_server_controller import (
    DeleteServerController,
)
from st_server.server.interface.controller.server.find_many_server_controller import (
    FindManyServerController,
)
from st_server.server.interface.controller.server.find_one_server_controller import (
    FindOneServerController,
)
from st_server.server.interface.controller.server.update_server_controller import (
    UpdateServerController,
)
from st_server.shared.application.query_response import QueryResponse

router = APIRouter()
auth_scheme = HTTPBearer()


@router.get("", response_model=QueryResponse)
def get_all(
    limit: int = Query(default=25),
    offset: int = Query(default=0),
    filter: str = Query(default="{}"),
    and_filter: str = Query(default="[]"),
    or_filter: str = Query(default="[]"),
    sort: str = Query(default="[]"),
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    """Route to get all servers."""
    query = FindManyServerQuery(
        limit=limit,
        offset=offset,
        filter=filter,
        and_filter=and_filter,
        or_filter=or_filter,
        sort=sort,
    )
    servers = FindManyServerController.handle(query)
    if servers.total == 0:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    return JSONResponse(
        content=jsonable_encoder(obj=servers),
        status_code=status.HTTP_200_OK,
    )


@router.get("/{id}", response_model=ServerReadDto)
def get(
    id: str,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    """Route to get a Server by id."""
    query = FindOneServerQuery(id=id)
    server = FindOneServerController.handle(query)
    return JSONResponse(
        content=jsonable_encoder(obj=server), status_code=status.HTTP_200_OK
    )


@router.post("", response_model=ServerReadDto)
def create(
    command: AddServerCommand,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    """Route to create a Server."""
    AddServerController.handle(command)
    return JSONResponse(
        content=jsonable_encoder(obj=command),
        status_code=status.HTTP_201_CREATED,
    )


@router.put("/{id}", response_model=ServerReadDto)
def update(
    id: str,
    command: UpdateServerCommand,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    """Route to update a Server."""
    UpdateServerController.handle(command)
    return JSONResponse(
        content=jsonable_encoder(obj=command),
        status_code=status.HTTP_200_OK,
    )


@router.delete("/{id}")
def delete(
    id: str,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    """Route to discard a Server."""
    command = DeleteServerCommand(id=id)
    DeleteServerController.handle(command)
    return JSONResponse(
        content=jsonable_encoder(
            obj={"message": "The Server has been deleted"}
        ),
        status_code=status.HTTP_200_OK,
    )
