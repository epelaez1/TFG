import pytest
from fastapi.routing import APIRoute
from starlette.routing import BaseRoute

from src.authentication.entrypoints.exception_handlers import auth_exc_handlers
from src.authentication.entrypoints.router import auth_router
from src.bootstrap import initialize_app
from src.profile.entrypoints.exception_handlers import profile_exc_handlers
from src.profile.entrypoints.router import profile_router
from src.service_info.entrypoints.router import service_info_router


@pytest.mark.parametrize(
    'api_routes',
    [
        service_info_router.routes,
        profile_router.routes,
        auth_router.routes,
    ],
)
def test_routes_included_in_app(api_routes: list[BaseRoute]):
    app = initialize_app()
    for route in api_routes:
        if isinstance(route, APIRoute) and route.name is not None:
            app.url_path_for(route.name)
        else:
            raise AssertionError('Route is not instance of APIRoute or has no name')


@pytest.mark.parametrize(
    'exc_handlers',
    [
        profile_exc_handlers,
        auth_exc_handlers,
    ],
)
def test_exc_handlers_included_in_app(exc_handlers):
    app = initialize_app()
    for exc in exc_handlers:
        assert exc in app.exception_handlers
