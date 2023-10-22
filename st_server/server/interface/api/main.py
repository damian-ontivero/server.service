"""API module."""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware import cors

from st_server.server.interface.api.exception import (
    EXCEPTION_TO_HTTP_STATUS_CODE,
)
from st_server.server.interface.api.router import application, server

app = FastAPI()

app.add_middleware(
    cors.CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(
    router=application.router,
    prefix="/server/applications",
    tags=["Application"],
)

app.include_router(
    router=server.router,
    prefix="/server/servers",
    tags=["Server"],
)


@app.middleware("http")
async def catch_exceptions(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as exception:
        if exception.__class__ in EXCEPTION_TO_HTTP_STATUS_CODE:
            raise HTTPException(
                status_code=EXCEPTION_TO_HTTP_STATUS_CODE[exception.__class__],
                detail=str(exception),
            )
        raise exception
