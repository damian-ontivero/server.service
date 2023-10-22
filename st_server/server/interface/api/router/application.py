"""Application router."""

from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from st_server.server.application.application.command.add_application_command import (
    AddApplicationCommand,
)
from st_server.server.application.application.command.delete_application_command import (
    DeleteApplicationCommand,
)
from st_server.server.application.application.command.update_application_command import (
    UpdateApplicationCommand,
)
from st_server.server.application.application.dto.application import (
    ApplicationReadDto,
)
from st_server.server.application.application.query.find_many_application_query import (
    FindManyApplicationQuery,
)
from st_server.server.application.application.query.find_one_application_query import (
    FindOneApplicationQuery,
)
from st_server.server.interface.controller.application.add_application_controller import (
    AddApplicationController,
)
from st_server.server.interface.controller.application.delete_application_controller import (
    DeleteApplicationController,
)
from st_server.server.interface.controller.application.find_many_application_controller import (
    FindManyApplicationController,
)
from st_server.server.interface.controller.application.find_one_application_controller import (
    FindOneApplicationController,
)
from st_server.server.interface.controller.application.update_application_controller import (
    UpdateApplicationController,
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
    applications = FindManyApplicationController.handle(query)
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
    application = FindOneApplicationController.handle(query)
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
    AddApplicationController.handle(command)
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
    UpdateApplicationController.handle(command)
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
    DeleteApplicationController.handle(command)
    return JSONResponse(
        content=jsonable_encoder(
            obj={"message": "The Application has been deleted"}
        ),
        status_code=status.HTTP_200_OK,
    )
