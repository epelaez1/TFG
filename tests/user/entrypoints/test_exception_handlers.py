import json

from fastapi import status
from fastapi.responses import JSONResponse

from src.error_models import APIError
from src.user.domain import exceptions
from src.user.entrypoints import exception_handlers


def test_unauthorized():
    assert exceptions.Unauthorized in exception_handlers.user_exc_handlers
    response: JSONResponse = exception_handlers.user_exc_handlers[exceptions.Unauthorized](None, None)
    error_details = APIError(**json.loads(response.body))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert error_details.error_code == exception_handlers.UNAUTHORIZED_ERROR_CODE


def test_user_already_registered():
    assert exceptions.UserAlreadyRegistered in exception_handlers.user_exc_handlers
    response: JSONResponse = exception_handlers.user_exc_handlers[exceptions.UserAlreadyRegistered](None, None)
    error_details = APIError(**json.loads(response.body))
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert error_details.error_code == exception_handlers.USER_ALREADY_REGISTERED_ERROR_CODE


def test_incorrect_username_or_password():
    assert exceptions.IncorrectPassword in exception_handlers.user_exc_handlers
    assert exceptions.IncorrectUsername in exception_handlers.user_exc_handlers
    response: JSONResponse = exception_handlers.user_exc_handlers[exceptions.IncorrectPassword](None, None)
    error_details = APIError(**json.loads(response.body))
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert error_details.error_code == exception_handlers.INCORRECT_USERNAME_OR_PASSWORD_ERROR_CODE


def test_user_does_not_exists():
    assert exceptions.UserDoesNotExists in exception_handlers.user_exc_handlers
    response: JSONResponse = exception_handlers.user_exc_handlers[exceptions.UserDoesNotExists](None, None)
    error_details = APIError(**json.loads(response.body))
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert error_details.error_code == exception_handlers.USER_DOES_NOT_EXISTS_ERROR_CODE
