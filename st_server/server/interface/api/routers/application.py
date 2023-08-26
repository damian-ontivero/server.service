"""Application router."""

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from st_server.server.application.dtos.application import (
    ApplicationCreateDto,
    ApplicationReadDto,
    ApplicationUpdateDto,
)
from st_server.server.application.services.application import (
    ApplicationService,
)
from st_server.server.infrastructure.message_bus.rabbitmq_message_bus import (
    RabbitMQMessageBus,
)
from st_server.server.infrastructure.mysql import db
from st_server.server.infrastructure.mysql.repositories.application_repository import (
    ApplicationRepositoryImpl,
)
from st_server.server.interface.api.query_parameters.application import (
    ApplicationQueryParameter,
)
from st_server.shared.application.exceptions import (
    AlreadyExists,
    AuthenticationError,
    FilterError,
    NotFound,
    PaginationError,
    SortError,
)

router = APIRouter()
auth_scheme = HTTPBearer()


def get_db_session():
    """Yields a database session."""
    session = db.SessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_application_repository(
    session: db.SessionLocal = Depends(get_db_session),
):
    """Yields a Application repository."""
    yield ApplicationRepositoryImpl(session=session)


def get_message_bus():
    """Yields a message bus."""
    yield RabbitMQMessageBus(
        host="localhost", port=5672, username="admin", password="admin"
    )


def get_application_service(
    repository: ApplicationRepositoryImpl = Depends(
        get_application_repository
    ),
    message_bus: RabbitMQMessageBus = Depends(get_message_bus),
):
    """Yields a Application service."""
    yield ApplicationService(repository=repository, message_bus=message_bus)


@router.get("", response_model=list[ApplicationReadDto])
def get_all(
    limit: int = Query(default=25),
    offset: int = Query(default=0),
    sort: list[str] | None = Query(default=None),
    filter: ApplicationQueryParameter = Depends(),
    fields: list[str] | None = Query(default=None),
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
    request: Request = None,
    application_service: ApplicationService = Depends(get_application_service),
):
    """Route to get all Applications."""
    try:
        applications = application_service.find_many(
            fields=fields,
            limit=limit,
            offset=offset,
            sort=sort,
            **filter.model_dump(exclude_none=True),
            access_token=authorization.credentials,
        )
        if not applications._items:
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
        return JSONResponse(
            content=jsonable_encoder(obj=applications),
            status_code=status.HTTP_200_OK,
        )
    except AuthenticationError as e:
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


@router.get("/{id}", response_model=ApplicationReadDto)
def get(
    id: str,
    fields: list[str] | None = Query(default=None),
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
    application_service: ApplicationService = Depends(get_application_service),
):
    """Route to get an Application by id."""
    try:
        application = application_service.find_one(
            id=id, fields=fields, access_token=authorization.credentials
        )
        return JSONResponse(content=jsonable_encoder(obj=application))
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=str(e)
        )
    except NotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )


@router.post("", response_model=ApplicationReadDto)
def create(
    application_in: ApplicationCreateDto,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
    application_service: ApplicationService = Depends(get_application_service),
):
    """Route to create an Application."""
    try:
        application = application_service.add_one(
            data=application_in.to_dict(),
            access_token=authorization.credentials,
        )
        return JSONResponse(
            content=jsonable_encoder(obj=application),
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


@router.put("/{id}", response_model=ApplicationReadDto)
def update(
    id: str,
    application_in: ApplicationUpdateDto,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
    application_service: ApplicationService = Depends(get_application_service),
):
    """Route to update an Application."""
    try:
        application = application_service.update_one(
            id=id,
            data=application_in.to_dict(),
            access_token=authorization.credentials,
        )
        return JSONResponse(
            content=jsonable_encoder(obj=application),
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
def discard(
    id: str,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
    application_service: ApplicationService = Depends(get_application_service),
):
    """Route to discard an Application."""
    try:
        application_service.discard_one(
            id=id, access_token=authorization.credentials
        )
        return JSONResponse(
            content=jsonable_encoder(obj={"message": "Server deleted"}),
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
