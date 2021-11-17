from typing import Callable
from typing import Type

from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse

from src.service_info.entrypoints import service_info_router
from src.user.entrypoints import user_router
from src.user.entrypoints.exception_handlers import user_exc_handlers


def add_routers(app: FastAPI) -> None:
    app.include_router(service_info_router.router)
    app.include_router(user_router.router)


def add_error_handlers(
    app: FastAPI,
    exc_handlers: dict[Type[Exception], Callable[[Request | None, Exception | None], JSONResponse]],
) -> None:
    for exc_type, exc_handler in exc_handlers.items():
        app.add_exception_handler(exc_type, exc_handler)


def initialize_app() -> FastAPI:
    app = FastAPI()
    add_routers(app)
    add_error_handlers(app, user_exc_handlers)
    return app
