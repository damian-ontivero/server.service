import json

from fastapi import APIRouter, Depends, Query, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from st_server.server.server.application.command.discard_server_command import (
    DiscardServerCommand,
)
from st_server.server.server.application.command.modify_server_command import (
    ModifyServerCommand,
)
from st_server.server.server.application.command.register_server_command import (
    RegisterServerCommand,
)
from st_server.server.server.application.dto.server import ServerDto
from st_server.server.server.application.query.find_many_server_query import (
    FindManyServerQuery,
)
from st_server.server.server.application.query.find_one_server_query import (
    FindOneServerQuery,
)
from st_server.shared.application.query_response import QueryResponse
from st_server.shared.domain.bus.command.command_bus import CommandBus
from st_server.shared.domain.bus.query.query_bus import QueryBus
from st_server.shared.infrastructure.ui.api.cqrs.command import (
    InMemoryCommandBus,
)
from st_server.shared.infrastructure.ui.api.cqrs.query import InMemoryQueryBus

router = APIRouter(prefix="/server/servers", tags=["Server"])
auth_scheme = HTTPBearer()


@router.get("", response_model=QueryResponse)
def get_all(
    limit: int = Query(default=25),
    offset: int = Query(default=0),
    filter: str = Query(default="{}"),
    and_filter: str = Query(default="[]"),
    or_filter: str = Query(default="[]"),
    sort: str = Query(default="[]"),
    query_bus: QueryBus = Depends(InMemoryQueryBus),
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    query = FindManyServerQuery(
        limit=limit,
        offset=offset,
        filter=json.loads(filter),
        and_filter=json.loads(and_filter),
        or_filter=json.loads(or_filter),
        sort=json.loads(sort),
    )
    servers = query_bus.ask(query)
    if servers.total == 0:
        return JSONResponse(content=[], status_code=status.HTTP_204_NO_CONTENT)
    return JSONResponse(
        content=jsonable_encoder(obj=servers),
        status_code=status.HTTP_200_OK,
    )


@router.get("/{id}", response_model=ServerDto)
def get(
    id: str,
    query_bus: QueryBus = Depends(InMemoryQueryBus),
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    query = FindOneServerQuery(id)
    server = query_bus.ask(query)
    return JSONResponse(
        content=jsonable_encoder(obj=server), status_code=status.HTTP_200_OK
    )


@router.post("", response_model=ServerDto)
def create(
    command: RegisterServerCommand,
    command_bus: CommandBus = Depends(InMemoryCommandBus),
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    command_bus.dispatch(command)
    return JSONResponse(
        content=jsonable_encoder(obj=command),
        status_code=status.HTTP_201_CREATED,
    )


@router.put("/{id}", response_model=ServerDto)
def update(
    id: str,
    command: ModifyServerCommand,
    command_bus: CommandBus = Depends(InMemoryCommandBus),
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    command_bus.dispatch(command)
    return JSONResponse(
        content=jsonable_encoder(obj=command),
        status_code=status.HTTP_200_OK,
    )


@router.delete("/{id}")
def delete(
    id: str,
    command_bus: CommandBus = Depends(InMemoryCommandBus),
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    command = DiscardServerCommand(id)
    command_bus.dispatch(command)
    return JSONResponse(
        content=jsonable_encoder(
            obj={"message": "The Server has been deleted"}
        ),
        status_code=status.HTTP_200_OK,
    )
