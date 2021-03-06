from fastapi import FastAPI

from src.authentication.entrypoints.exception_handlers import auth_exc_handlers
from src.authentication.entrypoints.router import auth_router
from src.profile.entrypoints.exception_handlers import profile_exc_handlers
from src.profile.entrypoints.router import profile_router
from src.service_info.entrypoints.router import service_info_router
from src.venue.entrypoints.exception_handlers import venue_exc_handlers
from src.venue.entrypoints.router import venue_router

all_routers = [
    service_info_router,
    profile_router,
    auth_router,
    venue_router,
]


all_exc_handlers = [
    profile_exc_handlers,
    auth_exc_handlers,
    venue_exc_handlers,
]


def add_routers(app: FastAPI) -> None:
    for router in all_routers:
        app.include_router(router)


def add_error_handlers(app: FastAPI) -> None:
    for exc_handlers in all_exc_handlers:
        for exc_type, exc_handler in exc_handlers.items():
            app.add_exception_handler(exc_type, exc_handler)


def initialize_app() -> FastAPI:
    app = FastAPI()
    add_routers(app)
    add_error_handlers(app)
    return app
