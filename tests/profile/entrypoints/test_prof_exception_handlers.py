import json

import pytest
from fastapi import status
from fastapi.responses import JSONResponse

from src.error_models import APIError
from src.profile.domain import exceptions
from src.profile.entrypoints import exception_handlers


@pytest.mark.parametrize(('exception', 'status_code', 'error_code'), [
    (
        exceptions.ProfileAlreadyInitialized,
        status.HTTP_400_BAD_REQUEST,
        exception_handlers.PROFILE_ALREADY_INITIALIZED,
    ),
    (exceptions.ProfileDoesNotExist, status.HTTP_400_BAD_REQUEST, exception_handlers.PROFILE_DOES_NOT_EXIST),
])
def test_profile_exceptions_are_handled(exception, status_code, error_code):
    assert exception in exception_handlers.profile_exc_handlers
    response: JSONResponse = exception_handlers.profile_exc_handlers[exception](None, None)
    error_details = APIError(**json.loads(response.body))
    assert response.status_code == status_code
    assert error_details.error_code == error_code
