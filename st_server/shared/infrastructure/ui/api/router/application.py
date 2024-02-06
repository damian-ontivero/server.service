import json

from fastapi import APIRouter, Depends, Query, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from st_server.server.application.application.command.discard_application_command import (
    DiscardApplicationCommand,
)
from st_server.server.application.application.command.modify_application_command import (
    ModifyApplicationCommand,
)
from st_server.server.application.application.command.register_application_command import (
    RegisterApplicationCommand,
)
from st_server.server.application.application.dto.application import (
    ApplicationDto,
)
from st_server.server.application.application.query.find_many_application_query import (
    FindManyApplicationQuery,
)
from st_server.server.application.application.query.find_one_application_query import (
    FindOneApplicationQuery,
)
from st_server.shared.application.query_response import QueryResponse
from st_server.shared.domain.bus.command.command_bus import CommandBus
from st_server.shared.domain.bus.query.query_bus import QueryBus
from st_server.shared.infrastructure.ui.api.cqrs.command import (
    InMemoryCommandBus,
)
from st_server.shared.infrastructure.ui.api.cqrs.query import InMemoryQueryBus

router = APIRouter(prefix="/server/applications", tags=["Application"])
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
    query = FindManyApplicationQuery(
        limit=limit,
        offset=offset,
        filter=json.loads(filter),
        and_filter=json.loads(and_filter),
        or_filter=json.loads(or_filter),
        sort=json.loads(sort),
    )
    applications = query_bus.ask(query)
    if applications.total == 0:
        return JSONResponse(content=[], status_code=status.HTTP_204_NO_CONTENT)
    return JSONResponse(
        content=jsonable_encoder(obj=applications),
        status_code=status.HTTP_200_OK,
    )


@router.get("/{id}", response_model=ApplicationDto)
def get(
    id: str,
    query_bus: QueryBus = Depends(InMemoryQueryBus),
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    query = FindOneApplicationQuery(id)
    application = query_bus.ask(query)
    return JSONResponse(
        content=jsonable_encoder(obj=application),
        status_code=status.HTTP_200_OK,
    )


@router.post("", response_model=ApplicationDto)
def create(
    command: RegisterApplicationCommand,
    command_bus: CommandBus = Depends(InMemoryCommandBus),
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    command_bus.dispatch(command)
    return JSONResponse(
        content=jsonable_encoder(obj=command),
        status_code=status.HTTP_201_CREATED,
    )


@router.put("/{id}", response_model=ApplicationDto)
def update(
    id: str,
    command: ModifyApplicationCommand,
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
    command = DiscardApplicationCommand(id)
    command_bus.dispatch(command)
    return JSONResponse(
        content=jsonable_encoder(
            obj={"message": "The Application has been deleted"}
        ),
        status_code=status.HTTP_200_OK,
    )
