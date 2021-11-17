import pytest
from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.routing import BaseRoute

from src.bootstrap import add_routers
from src.bootstrap import initialize_app
from src.service_info.entrypoints import service_info_router
from src.user.entrypoints import user_router
from src.user.entrypoints.exception_handlers import user_exc_handlers


@pytest.mark.parametrize(
    'api_routes',
    [
        service_info_router.router.routes,
        user_router.router.routes,
    ],
)
def test_routes_included_in_app(api_routes: list[BaseRoute]):
    app = FastAPI()
    add_routers(app)
    for route in api_routes:
        if isinstance(route, APIRoute) and route.name is not None:
            app.url_path_for(route.name)
        else:
            raise AssertionError('Route is not instance of APIRoute or has no name')


@pytest.mark.parametrize(
    'exc_handlers',
    [
        user_exc_handlers,
    ],
)
def test_exc_handlers_included_in_app(exc_handlers):
    app = initialize_app()

    for exc in exc_handlers:
        assert exc in app.exception_handlers
