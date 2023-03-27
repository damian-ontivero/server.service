"""Doc."""

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from st_server.application.app.connection_type.schema import (
    ConnectionTypeQueryParams,
)
from st_server.application.helper.filter import FilterFormatError
from st_server.application.helper.pagination import (
    PageLessThanOne,
    PageNotAnInteger,
    PerPageLessThanZero,
    PerPageNotAnInteger,
)
from st_server.application.helper.sort import SortFormatError
from st_server.application.service.connection_type import ConnectionTypeService
from st_server.domain.connection_type import (
    ConnectionType,
    ConnectionTypeCreate,
    ConnectionTypeNameAlreadyExists,
    ConnectionTypeNotFound,
    ConnectionTypeUpdate,
)

router = APIRouter()
auth_scheme = HTTPBearer()


@router.get("")
def get_all(
    per_page: int = Query(default=25),
    page: int = Query(default=1),
    sort: list[str] | None = Query(default=None),
    filter: ConnectionTypeQueryParams = Depends(),
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
    request: Request = None,
):
    """Doc."""
    try:
        connection_types = ConnectionTypeService.find_many(
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
            prev_page = '<{0}server/connection-types?per_page={1}&page={2}>; rel="prev", '.format(
                base_url, connection_types.per_page, connection_types.prev_page
            )
            link += prev_page

        if connection_types.next_page:
            next_page = '<{0}server/connection-types?per_page={1}&page={2}>; rel="next", '.format(
                base_url, connection_types.per_page, connection_types.next_page
            )
            link += next_page

        if connection_types.last_page:
            last_page = f'<{0}server/connection-types?per_page={1}&page={2}>; rel="last", '.format(
                base_url, connection_types.per_page, connection_types.last_page
            )
            link += last_page

        if connection_types.first_page:
            first_page = f'<{0}server/connection-types?per_page={1}&page={2}>; rel="first"'.format(
                base_url,
                connection_types.per_page,
                connection_types.first_page,
            )
            link += first_page

        response = JSONResponse(
            content=jsonable_encoder(obj=connection_types.items)
        )
        response.headers["Link"] = link

        return response

    except PageLessThanOne as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )

    except PageNotAnInteger as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )

    except PerPageLessThanZero as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )

    except PerPageNotAnInteger as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )

    except SortFormatError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )

    except FilterFormatError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


@router.get("/{id_}", response_model=ConnectionType)
def get(
    id_: int,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    """Doc."""
    try:
        connection_type = ConnectionTypeService.find_one(
            id_=id_, access_token=authorization.credentials
        )

        return JSONResponse(content=jsonable_encoder(obj=connection_type))

    except ConnectionTypeNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )


@router.post("", response_model=ConnectionType)
def create(
    connection_type_in: ConnectionTypeCreate,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    """Doc."""
    try:
        connection_type = ConnectionTypeService.add_one(
            connection_type_dto=connection_type_in,
            access_token=authorization.credentials,
        )

        return JSONResponse(content=jsonable_encoder(obj=connection_type))

    except ConnectionTypeNameAlreadyExists as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        )


@router.put("/{id_}", response_model=ConnectionType)
def update(
    id_: int,
    connection_type_in: ConnectionTypeUpdate,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    """Doc."""
    try:
        connection_type = ConnectionTypeService.update_one(
            id_=id_,
            connection_type_dto=connection_type_in,
            access_token=authorization.credentials,
        )

        return JSONResponse(content=jsonable_encoder(obj=connection_type))

    except ConnectionTypeNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )

    except ConnectionTypeNameAlreadyExists as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        )


@router.delete("/{id_}", response_model=ConnectionType)
def delete(
    id_: int,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    """Doc."""
    try:
        connection_type = ConnectionTypeService.delete_one(
            id_=id_, access_token=authorization.credentials
        )

        return JSONResponse(content=jsonable_encoder(obj=connection_type))

    except ConnectionTypeNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
