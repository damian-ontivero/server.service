"""Application router."""

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from st_server.context.server.application.service.application import (
    ApplicationService,
)
from st_server.context.server.infrastructure.message_bus.rabbitmq_message_bus import (
    RabbitMQMessageBus,
)
from st_server.context.server.infrastructure.mysql import db
from st_server.context.server.infrastructure.mysql.application.application_repository import (
    ApplicationRepository,
)
from st_server.context.server.interface.api.application.query_parameter import (
    ApplicationQueryParameter,
)
from st_server.context.server.interface.api.application.schema import (
    ApplicationCreate,
    ApplicationRead,
    ApplicationUpdate,
)
from st_server.shared.core.exception import (
    AlreadyExists,
    AuthenticationError,
    FilterError,
    NotFound,
    PaginationError,
    SortError,
)

router = APIRouter()
auth_scheme = HTTPBearer()


def get_session():
    """Yield a database session."""
    session = db.SessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_application_repository(
    session: db.SessionLocal = Depends(get_session),
):
    """Yield a application repository."""
    yield ApplicationRepository(session=session)


def get_message_bus():
    """Yield a message bus."""
    yield RabbitMQMessageBus(
        host="localhost",
        port=5672,
        username="admin",
        password="admin",
    )


def get_application_service(
    repository: ApplicationRepository = Depends(get_application_repository),
    message_bus: RabbitMQMessageBus = Depends(get_message_bus),
):
    """Yield a application service."""
    yield ApplicationService(repository=repository, message_bus=message_bus)


@router.get("", response_model=list[ApplicationRead])
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
    """Doc."""
    try:
        applications = application_service.find_many(
            fields=fields,
            limit=limit,
            offset=offset,
            sort=sort,
            **filter.dict(exclude_none=True),
            access_token=authorization.credentials,
        )

        if not applications.items:
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)

        base_url = request.base_url
        link = ""

        if applications.prev_offset:
            prev_offset = f'<{base_url}server/applications?limit={applications.limit}&offset={applications.prev_offset}>; rel="prev", '
            link += prev_offset

        if applications.next_offset:
            next_offset = f'<{base_url}server/applications?limit={applications.limit}&offset={applications.next_offset}>; rel="next", '
            link += next_offset

        if applications.last_offset:
            last_offset = f'<{base_url}server/applications?limit={applications.limit}&offset={applications.last_offset}>; rel="last", '
            link += last_offset

        if applications.first_offset:
            first_offset = f'<{base_url}server/applications?limit={applications.limit}&offset={applications.first_offset}>; rel="first"'
            link += first_offset

        response = JSONResponse(
            content=jsonable_encoder(
                obj=[
                    ApplicationRead(**application.to_dict())
                    for application in applications.items
                ]
            )
        )
        response.headers["Link"] = link

        return response

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


@router.get("/{id}", response_model=ApplicationRead)
def get(
    id: str,
    fields: list[str] | None = Query(default=None),
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
    application_service: ApplicationService = Depends(get_application_service),
):
    """Doc."""
    try:
        application = application_service.find_one(
            id=id, fields=fields, access_token=authorization.credentials
        )

        return JSONResponse(
            content=jsonable_encoder(
                obj=ApplicationRead(**application.to_dict())
            )
        )

    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=str(e)
        )

    except NotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )


@router.post("", response_model=ApplicationRead)
def create(
    application_in: ApplicationCreate,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    """Doc."""
    try:
        session = db.SessionLocal()
        repository = ApplicationRepository(session=session)
        message_bus = RabbitMQMessageBus(
            host="localhost",
            port=5672,
            username="admin",
            password="admin",
        )
        application_service = ApplicationService(
            repository=repository, message_bus=message_bus
        )

        application = application_service.add_one(
            data=application_in.to_dict(),
            access_token=authorization.credentials,
        )

        return JSONResponse(
            content=jsonable_encoder(
                obj=ApplicationRead(**application.to_dict())
            ),
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


@router.put("/{id}", response_model=ApplicationRead)
def update(
    id: str,
    application_in: ApplicationUpdate,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    """Doc."""
    try:
        session = db.SessionLocal()
        repository = ApplicationRepository(session=session)
        message_bus = RabbitMQMessageBus(
            host="localhost",
            port=5672,
            username="admin",
            password="admin",
        )
        application_service = ApplicationService(
            repository=repository, message_bus=message_bus
        )

        application = application_service.update_one(
            id=id,
            data=application_in.to_dict(),
            access_token=authorization.credentials,
        )

        return JSONResponse(
            content=jsonable_encoder(
                obj=ApplicationRead(**application.to_dict())
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

    except AlreadyExists as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        )


@router.delete("/{id}")
def discard(
    id: str, authorization: HTTPAuthorizationCredentials = Depends(auth_scheme)
):
    """Doc."""
    try:
        session = db.SessionLocal()
        repository = ApplicationRepository(session=session)
        message_bus = RabbitMQMessageBus(
            host="localhost",
            port=5672,
            username="admin",
            password="admin",
        )
        application_service = ApplicationService(
            repository=repository, message_bus=message_bus
        )

        application_service.discard_one(
            id=id, access_token=authorization.credentials
        )

        return JSONResponse(
            content=jsonable_encoder(obj={"message": "User deleted"}),
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
