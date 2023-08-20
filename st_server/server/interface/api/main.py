"""API module."""

from fastapi import FastAPI
from fastapi.middleware import cors

from st_server.server.interface.api.routers.application import (
    router as application_router,
)
from st_server.server.interface.api.routers.credential import (
    router as credential_router,
)
from st_server.server.interface.api.routers.server import (
    router as server_router,
)

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
    router=application_router,
    prefix="/server/applications",
    tags=["Application"],
)

app.include_router(
    router=server_router,
    prefix="/server/servers",
    tags=["Server"],
)

app.include_router(
    router=credential_router,
    prefix="/server/credentials",
    tags=["Credential"],
)
