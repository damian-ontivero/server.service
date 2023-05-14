"""Server router."""

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from st_server.application.service.connection_type import ConnectionTypeService
from st_server.domain.exception import (
    AlreadyExists,
    AuthenticationError,
    FilterError,
    NotFound,
    PaginationError,
    SortError,
)
from st_server.infrastructure.message_bus.rabbitmq_message_bus import (
    RabbitMQMessageBus,
)
from st_server.infrastructure.mysql import db
from st_server.infrastructure.mysql.connection_type.connection_type_repository import (
    ConnectionTypeRepository,
)
from st_server.interface.api.connection_type.query_parameter import (
    ConnectionTypeQueryParameter,
)
from st_server.interface.api.connection_type.schema import (
    ConnectionTypeCreate,
    ConnectionTypeRead,
    ConnectionTypeUpdate,
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


def get_connection_type_repository(
    session: db.SessionLocal = Depends(get_session),
):
    """Yield a connection type repository."""
    yield ConnectionTypeRepository(session=session)


def get_message_bus():
    """Yield a message bus."""
    yield RabbitMQMessageBus(
        host="localhost",
        port=5672,
        username="admin",
        password="admin",
    )


def get_connection_type_service(
    repository: ConnectionTypeRepository = Depends(
        get_connection_type_repository
    ),
    message_bus: RabbitMQMessageBus = Depends(get_message_bus),
):
    """Yield a connection type service."""
    yield ConnectionTypeService(repository=repository, message_bus=message_bus)


@router.get("", response_model=list[ConnectionTypeRead])
def get_all(
    per_page: int = Query(default=25),
    page: int = Query(default=1),
    sort: list[str] | None = Query(default=None),
    filter: ConnectionTypeQueryParameter = Depends(),
    fields: list[str] | None = Query(default=None),
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
    request: Request = None,
    connection_type_service: ConnectionTypeService = Depends(
        get_connection_type_service
    ),
):
    """Doc."""
    try:
        connection_types = connection_type_service.find_many(
            fields=fields,
            per_page=per_page,
            page=page,
            sort=sort,
            **filter.dict(exclude_none=True),
            access_token=authorization.credentials,
        )

        if not connection_types.items:
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)

        base_url = request.base_url
        link = ""

        if connection_types.prev_page:
            prev_page = f'<{base_url}support/connection-types?per_page={connection_types.per_page}&page={connection_types.prev_page}>; rel="prev", '
            link += prev_page

        if connection_types.next_page:
            next_page = f'<{base_url}support/connection-types?per_page={connection_types.per_page}&page={connection_types.next_page}>; rel="next", '
            link += next_page

        if connection_types.last_page:
            last_page = f'<{base_url}support/connection-types?per_page={connection_types.per_page}&page={connection_types.last_page}>; rel="last", '
            link += last_page

        if connection_types.first_page:
            first_page = f'<{base_url}support/connection-types?per_page={connection_types.per_page}&page={connection_types.first_page}>; rel="first"'
            link += first_page

        response = JSONResponse(
            content=jsonable_encoder(
                obj=[
                    ConnectionTypeRead(**connection_type.to_dict())
                    for connection_type in connection_types.items
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


@router.get("/{id}", response_model=ConnectionTypeRead)
def get(
    id: str,
    fields: list[str] | None = Query(default=None),
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
    connection_type_service: ConnectionTypeService = Depends(
        get_connection_type_service
    ),
):
    """Doc."""
    try:
        connection_type = connection_type_service.find_one(
            id=id, fields=fields, access_token=authorization.credentials
        )

        return JSONResponse(
            content=jsonable_encoder(
                obj=ConnectionTypeRead(**connection_type.to_dict())
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


@router.post("", response_model=ConnectionTypeRead)
def create(
    connection_type_in: ConnectionTypeCreate,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    """Doc."""
    try:
        session = db.SessionLocal()
        repository = ConnectionTypeRepository(session=session)
        message_bus = RabbitMQMessageBus(
            host="localhost",
            port=5672,
            username="admin",
            password="admin",
        )
        connection_type_service = ConnectionTypeService(
            repository=repository, message_bus=message_bus
        )

        connection_type = connection_type_service.add_one(
            data=connection_type_in.to_dict(),
            access_token=authorization.credentials,
        )

        return JSONResponse(
            content=jsonable_encoder(
                obj=ConnectionTypeRead(**connection_type.to_dict())
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


@router.put("/{id}", response_model=ConnectionTypeRead)
def update(
    id: str,
    connection_type_in: ConnectionTypeUpdate,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    """Doc."""
    try:
        session = db.SessionLocal()
        repository = ConnectionTypeRepository(session=session)
        message_bus = RabbitMQMessageBus(
            host="localhost",
            port=5672,
            username="admin",
            password="admin",
        )
        connection_type_service = ConnectionTypeService(
            repository=repository, message_bus=message_bus
        )

        connection_type = connection_type_service.update_one(
            id=id,
            data=connection_type_in.to_dict(),
            access_token=authorization.credentials,
        )

        return JSONResponse(
            content=jsonable_encoder(
                obj=ConnectionTypeRead(**connection_type.to_dict())
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
        repository = ConnectionTypeRepository(session=session)
        message_bus = RabbitMQMessageBus(
            host="localhost",
            port=5672,
            username="admin",
            password="admin",
        )
        connection_type_service = ConnectionTypeService(
            repository=repository, message_bus=message_bus
        )

        connection_type_service.discard_one(
            id=id, access_token=authorization.credentials
        )

        return JSONResponse(
            content=jsonable_encoder(
                obj={"message": "Connection type deleted"}
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
