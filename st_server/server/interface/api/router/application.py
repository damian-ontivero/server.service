"""Application router."""

import json

from fastapi import APIRouter, Depends, Query, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from st_server.server.application.application.command.add_application_command import (
    AddApplicationCommand,
)
from st_server.server.application.application.command.add_application_command_handler import (
    AddApplicationCommandHandler,
)
from st_server.server.application.application.command.delete_application_command import (
    DeleteApplicationCommand,
)
from st_server.server.application.application.command.delete_application_command_handler import (
    DeleteApplicationCommandHandler,
)
from st_server.server.application.application.command.update_application_command import (
    UpdateApplicationCommand,
)
from st_server.server.application.application.command.update_application_command_handler import (
    UpdateApplicationCommandHandler,
)
from st_server.server.application.application.dto.application import (
    ApplicationReadDto,
)
from st_server.server.application.application.query.find_many_query import (
    FindManyApplicationQuery,
)
from st_server.server.application.application.query.find_many_query_handler import (
    FindManyApplicationQueryHandler,
)
from st_server.server.application.application.query.find_one_query import (
    FindOneApplicationQuery,
)
from st_server.server.application.application.query.find_one_query_handler import (
    FindOneApplicationQueryHandler,
)
from st_server.shared.application.query_response import QueryResponse

router = APIRouter()
auth_scheme = HTTPBearer()


@router.get("", response_model=QueryResponse)
def get_all(
    query: FindManyApplicationQuery,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    """Route to get all applications."""
    applications = FindManyApplicationQueryHandler().handle(query)
    if applications.total == 0:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    return JSONResponse(
        content=jsonable_encoder(obj=applications),
        status_code=status.HTTP_200_OK,
    )


@router.get("/{id}", response_model=ApplicationReadDto)
def get(
    query: FindOneApplicationQuery,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    """Route to get an Application by id."""
    application = FindOneApplicationQueryHandler().handle(query)
    return JSONResponse(
        content=jsonable_encoder(obj=application),
        status_code=status.HTTP_200_OK,
    )


@router.post("", response_model=ApplicationReadDto)
def create(
    command: AddApplicationCommand,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    """Route to create an Application."""
    AddApplicationCommandHandler().handle(command)
    return JSONResponse(
        content=jsonable_encoder(obj=command),
        status_code=status.HTTP_201_CREATED,
    )


@router.put("/{id}", response_model=ApplicationReadDto)
def update(
    command: UpdateApplicationCommand,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    """Route to update an Application."""
    UpdateApplicationCommandHandler().handle(command)
    return JSONResponse(
        content=jsonable_encoder(obj=command),
        status_code=status.HTTP_200_OK,
    )


@router.delete("/{id}")
def delete(
    command: DeleteApplicationCommand,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    """Route to delete an Application."""
    DeleteApplicationCommandHandler().handle(command)
    return JSONResponse(
        content=jsonable_encoder(
            obj={"message": "The Application has been deleted"}
        ),
        status_code=status.HTTP_200_OK,
    )
