import json

import pytest
from fastapi import status
from fastapi.responses import JSONResponse

from src.authentication.domain import exceptions
from src.authentication.entrypoints import exception_handlers
from src.error_models import APIError


@pytest.mark.parametrize(('exception', 'status_code', 'error_code'), [
    (exceptions.Unauthorized, status.HTTP_401_UNAUTHORIZED, exception_handlers.UNAUTHORIZED),
    (exceptions.UserAlreadyRegistered, status.HTTP_400_BAD_REQUEST, exception_handlers.USER_ALREADY_REGISTERED),
    (exceptions.IncorrectPassword, status.HTTP_400_BAD_REQUEST, exception_handlers.INCORRECT_USERNAME_OR_PASSWORD),
    (exceptions.IncorrectUsername, status.HTTP_400_BAD_REQUEST, exception_handlers.INCORRECT_USERNAME_OR_PASSWORD),
    (exceptions.UserDoesNotExist, status.HTTP_400_BAD_REQUEST, exception_handlers.USER_DOES_NOT_EXIST),
    (exceptions.UserEmailNotVerified, status.HTTP_401_UNAUTHORIZED, exception_handlers.USER_EMAIL_NOT_VERIFIED),
    (exceptions.UserWithoutProfile, status.HTTP_401_UNAUTHORIZED, exception_handlers.USER_WITHOT_PROFILE),
])
def test_auth_exceptions_are_handled(exception, status_code, error_code):
    assert exception in exception_handlers.auth_exc_handlers
    response: JSONResponse = exception_handlers.auth_exc_handlers[exception](None, None)
    error_details = APIError(**json.loads(response.body))
    assert response.status_code == status_code
    assert error_details.error_code == error_code
