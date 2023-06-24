"""Server router."""

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from st_server.context.server.application.service.environment import (
    EnvironmentService,
)
from st_server.context.server.infrastructure.message_bus.rabbitmq_message_bus import (
    RabbitMQMessageBus,
)
from st_server.context.server.infrastructure.mysql import db
from st_server.context.server.infrastructure.mysql.repository.environment_repository import (
    EnvironmentRepository,
)
from st_server.context.server.interface.api.environment.schema import (
    EnvironmentCreate,
    EnvironmentRead,
    EnvironmentUpdate,
)
from st_server.context.server.interface.api.server.query_parameter import (
    ServerQueryParameter,
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
    session = db.SessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_environment_repository(
    session: db.SessionLocal = Depends(get_session),
):
    yield EnvironmentRepository(session=session)


def get_message_bus():
    yield RabbitMQMessageBus(
        host="localhost",
        port=5672,
        username="admin",
        password="admin",
    )


def get_environment_service(
    repository: EnvironmentRepository = Depends(get_environment_repository),
    message_bus: RabbitMQMessageBus = Depends(get_message_bus),
):
    yield EnvironmentService(repository=repository, message_bus=message_bus)


@router.get("", response_model=list[EnvironmentRead])
def get_all(
    limit: int = Query(default=25),
    offset: int = Query(default=0),
    sort: list[str] | None = Query(default=None),
    filter: ServerQueryParameter = Depends(),
    fields: list[str] | None = Query(default=None),
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
    request: Request = None,
    environment_service: EnvironmentService = Depends(get_environment_service),
):
    try:
        environments = environment_service.find_many(
            fields=fields,
            limit=limit,
            offset=offset,
            sort=sort,
            **filter.dict(exclude_none=True),
            access_token=authorization.credentials,
        )
        if not environments.items:
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
        base_url = request.base_url
        link = ""
        if environments.prev_offset:
            prev_offset = f'<{base_url}server/environments?limit={environments.limit}&offset={environments.prev_offset}>; rel="prev", '
            link += prev_offset
        if environments.next_offset:
            next_offset = f'<{base_url}server/environments?limit={environments.limit}&offset={environments.next_offset}>; rel="next", '
            link += next_offset
        if environments.last_offset:
            last_offset = f'<{base_url}server/environments?limit={environments.limit}&offset={environments.last_offset}>; rel="last", '
            link += last_offset
        if environments.first_offset:
            first_offset = f'<{base_url}server/environments?limit={environments.limit}&offset={environments.first_offset}>; rel="first"'
            link += first_offset
        response = JSONResponse(
            content=jsonable_encoder(
                obj=[
                    EnvironmentRead(**environment.to_dict())
                    for environment in environments.items
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


@router.get("/{id}", response_model=EnvironmentRead)
def get(
    id: str,
    fields: list[str] | None = Query(default=None),
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
    environment_service: EnvironmentService = Depends(get_environment_service),
):
    try:
        environment = environment_service.find_one(
            id=id, fields=fields, access_token=authorization.credentials
        )
        return JSONResponse(
            content=jsonable_encoder(
                obj=EnvironmentRead(**environment.to_dict())
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


@router.post("", response_model=EnvironmentRead)
def create(
    environment_in: EnvironmentCreate,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    try:
        session = db.SessionLocal()
        repository = EnvironmentRepository(session=session)
        message_bus = RabbitMQMessageBus(
            host="localhost",
            port=5672,
            username="admin",
            password="admin",
        )
        environment_service = EnvironmentService(
            repository=repository, message_bus=message_bus
        )
        environment = environment_service.add_one(
            data=environment_in.to_dict(),
            access_token=authorization.credentials,
        )
        return JSONResponse(
            content=jsonable_encoder(
                obj=EnvironmentRead(**environment.to_dict())
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


@router.put("/{id}", response_model=EnvironmentRead)
def update(
    id: str,
    environment_in: EnvironmentUpdate,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    try:
        session = db.SessionLocal()
        repository = EnvironmentRepository(session=session)
        message_bus = RabbitMQMessageBus(
            host="localhost",
            port=5672,
            username="admin",
            password="admin",
        )
        environment_service = EnvironmentService(
            repository=repository, message_bus=message_bus
        )
        environment = environment_service.update_one(
            id=id,
            data=environment_in.to_dict(),
            access_token=authorization.credentials,
        )
        return JSONResponse(
            content=jsonable_encoder(
                obj=EnvironmentRead(**environment.to_dict())
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
    try:
        session = db.SessionLocal()
        repository = EnvironmentRepository(session=session)
        message_bus = RabbitMQMessageBus(
            host="localhost",
            port=5672,
            username="admin",
            password="admin",
        )
        environment_service = EnvironmentService(
            repository=repository, message_bus=message_bus
        )
        environment_service.discard_one(
            id=id, access_token=authorization.credentials
        )
        return JSONResponse(
            content=jsonable_encoder(obj={"message": "Environment deleted"}),
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