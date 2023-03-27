"""Doc."""

from fastapi import FastAPI
from fastapi.middleware import cors

from st_server.application.app import (
    application,
    connection_type,
    environment,
    operating_system,
    server,
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
    router=application.router,
    prefix="/server/applications",
    tags=["Application"],
)
app.include_router(
    router=connection_type.router,
    prefix="/server/connection-types",
    tags=["Connection Type"],
)
app.include_router(
    router=environment.router,
    prefix="/server/environments",
    tags=["Environment"],
)
app.include_router(
    router=operating_system.router,
    prefix="/server/operating-systems",
    tags=["Operating System"],
)
app.include_router(
    router=server.router, prefix="/server/servers", tags=["Server"]
)
