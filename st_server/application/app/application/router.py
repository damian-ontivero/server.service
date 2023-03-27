"""Doc."""

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from st_server.application.app.application.schema import ApplicationQueryParams
from st_server.application.helper.filter import FilterFormatError
from st_server.application.helper.pagination import (
    PageLessThanOne,
    PageNotAnInteger,
    PerPageLessThanZero,
    PerPageNotAnInteger,
)
from st_server.application.helper.sort import SortFormatError
from st_server.application.service.application import ApplicationService
from st_server.domain.application import (
    Application,
    ApplicationCreate,
    ApplicationNameAlreadyExists,
    ApplicationNotFound,
    ApplicationUpdate,
)

router = APIRouter()
auth_scheme = HTTPBearer()


@router.get("")
def get_all(
    per_page: int = Query(default=25),
    page: int = Query(default=1),
    sort: list[str] | None = Query(default=None),
    filter: ApplicationQueryParams = Depends(),
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
    request: Request = None,
):
    """Doc."""
    try:
        applications = ApplicationService.find_many(
            per_page=per_page,
            page=page,
            sort=sort,
            **filter.dict(exclude_none=True),
            access_token=authorization.credentials,
        )

        if not applications.items:
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)

        base_url = request.base_url
        link = ""

        if applications.prev_page:
            prev_page = '<{0}server/applications?per_page={1}&page={2}>; rel="prev", '.format(
                base_url, applications.per_page, applications.prev_page
            )
            link += prev_page

        if applications.next_page:
            next_page = '<{0}server/applications?per_page={1}&page={2}>; rel="next", '.format(
                base_url, applications.per_page, applications.next_page
            )
            link += next_page

        if applications.last_page:
            last_page = f'<{0}server/applications?per_page={1}&page={2}>; rel="last", '.format(
                base_url, applications.per_page, applications.last_page
            )
            link += last_page

        if applications.first_page:
            first_page = f'<{0}server/applications?per_page={1}&page={2}>; rel="first"'.format(
                base_url, applications.per_page, applications.first_page
            )
            link += first_page

        response = JSONResponse(
            content=jsonable_encoder(obj=applications.items)
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


@router.get("/{id_}", response_model=Application)
def get(
    id_: int,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    """Doc."""
    try:
        application = ApplicationService.find_one(
            id_=id_, access_token=authorization.credentials
        )

        return JSONResponse(content=jsonable_encoder(obj=application))

    except ApplicationNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )


@router.post("", response_model=Application)
def create(
    application_in: ApplicationCreate,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    """Doc."""
    try:
        application = ApplicationService.add_one(
            application_dto=application_in,
            access_token=authorization.credentials,
        )

        return JSONResponse(content=jsonable_encoder(obj=application))

    except ApplicationNameAlreadyExists as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        )


@router.put("/{id_}", response_model=Application)
def update(
    id_: int,
    application_in: ApplicationUpdate,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    """Doc."""
    try:
        application = ApplicationService.update_one(
            id_=id_,
            application_dto=application_in,
            access_token=authorization.credentials,
        )

        return JSONResponse(content=jsonable_encoder(obj=application))

    except ApplicationNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )

    except ApplicationNameAlreadyExists as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        )


@router.delete("/{id_}", response_model=Application)
def delete(
    id_: int,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    """Doc."""
    try:
        application = ApplicationService.delete_one(
            id_=id_, access_token=authorization.credentials
        )

        return JSONResponse(content=jsonable_encoder(obj=application))

    except ApplicationNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
