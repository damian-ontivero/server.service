"""Doc."""

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from st_server.application.app.server.schema import ServerQueryParams
from st_server.application.helper.filter import FilterFormatError
from st_server.application.helper.pagination import (
    PageLessThanOne,
    PageNotAnInteger,
    PerPageLessThanZero,
    PerPageNotAnInteger,
)
from st_server.application.helper.sort import SortFormatError
from st_server.application.service.server.server import ServerService
from st_server.domain.server import (
    Server,
    ServerCreate,
    ServerNameAlreadyExists,
    ServerNotFound,
    ServerUpdate,
)

router = APIRouter()
auth_scheme = HTTPBearer()


@router.get("")
def get_all(
    per_page: int = Query(default=25),
    page: int = Query(default=1),
    sort: list[str] | None = Query(default=None),
    filter: ServerQueryParams = Depends(),
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
    request: Request = None,
):
    """Doc."""
    try:
        servers = ServerService.find_many(
            per_page=per_page,
            page=page,
            sort=sort,
            **filter.dict(exclude_none=True),
            access_token=authorization.credentials,
        )

        if not servers.items:
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)

        base_url = request.base_url
        link = ""

        if servers.prev_page:
            prev_page = '<{0}server/servers?per_page={1}&page={2}>; rel="prev", '.format(
                base_url, servers.per_page, servers.prev_page
            )
            link += prev_page

        if servers.next_page:
            next_page = '<{0}server/servers?per_page={1}&page={2}>; rel="next", '.format(
                base_url, servers.per_page, servers.next_page
            )
            link += next_page

        if servers.last_page:
            last_page = f'<{0}server/servers?per_page={1}&page={2}>; rel="last", '.format(
                base_url, servers.per_page, servers.last_page
            )
            link += last_page

        if servers.first_page:
            first_page = f'<{0}server/servers?per_page={1}&page={2}>; rel="first"'.format(
                base_url,
                servers.per_page,
                servers.first_page,
            )
            link += first_page
        response = JSONResponse(content=jsonable_encoder(obj=servers.items))
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


@router.get("/{id_}", response_model=Server)
def get(
    id_: int,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    """Doc."""
    try:
        server = ServerService.find_one(
            id_=id_, access_token=authorization.credentials
        )

        return JSONResponse(content=jsonable_encoder(obj=server))

    except ServerNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )


@router.post("", response_model=Server)
def create(
    server_in: ServerCreate,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    """Doc."""
    try:
        server = ServerService.add_one(
            server_dto=server_in,
            access_token=authorization.credentials,
        )

        return JSONResponse(content=jsonable_encoder(obj=server))

    except ServerNameAlreadyExists as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        )


@router.put("/{id_}", response_model=Server)
def update(
    id_: int,
    server_in: ServerUpdate,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    """Doc."""
    try:
        server = ServerService.update_one(
            id_=id_,
            server_dto=server_in,
            access_token=authorization.credentials,
        )

        return JSONResponse(content=jsonable_encoder(obj=server))

    except ServerNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )

    except ServerNameAlreadyExists as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        )


@router.delete("/{id_}", response_model=Server)
def delete(
    id_: int,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    """Doc."""
    try:
        server = ServerService.delete_one(
            id_=id_, access_token=authorization.credentials
        )

        return JSONResponse(content=jsonable_encoder(obj=server))

    except ServerNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
