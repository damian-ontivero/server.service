"""API module."""

from fastapi import FastAPI
from fastapi.middleware import cors

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
