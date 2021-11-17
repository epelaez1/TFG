from typing import Callable
from typing import Type

from fastapi import Request
from fastapi import status
from fastapi.responses import JSONResponse

from src.error_models import APIError
from src.user.domain import exceptions


UNAUTHORIZED_ERROR_CODE = 101
unauthorized_response = JSONResponse(
    APIError(detail='Could not validate credentials', error_code=UNAUTHORIZED_ERROR_CODE).dict(),
    status_code=status.HTTP_401_UNAUTHORIZED,
    headers={'WWW-Authenticate': 'Bearer'},
)

USER_ALREADY_REGISTERED_ERROR_CODE = 102
user_already_registered_response = JSONResponse(
    APIError(detail='User already exists', error_code=USER_ALREADY_REGISTERED_ERROR_CODE).dict(),
    status_code=status.HTTP_400_BAD_REQUEST,
)

INCORRECT_USERNAME_OR_PASSWORD_ERROR_CODE = 103
incorrect_username_or_password_response = JSONResponse(
    APIError(
        detail='Incorrect username or password',
        error_code=INCORRECT_USERNAME_OR_PASSWORD_ERROR_CODE,
    ).dict(),
    status_code=status.HTTP_400_BAD_REQUEST,
    headers={'WWW-Authenticate': 'Bearer'},
)

USER_DOES_NOT_EXISTS_ERROR_CODE = 104
user_does_not_exists_response = JSONResponse(
    APIError(detail='User does not exists', error_code=USER_DOES_NOT_EXISTS_ERROR_CODE).dict(),
    status_code=status.HTTP_400_BAD_REQUEST,
    headers={'WWW-Authenticate': 'Bearer'},
)

user_exc_handlers: dict[Type[Exception], Callable[[Request | None, Exception | None], JSONResponse]] = {
    exceptions.Unauthorized: lambda req, exc: unauthorized_response,
    exceptions.UserAlreadyRegistered: lambda req, exc: user_already_registered_response,
    exceptions.UserDoesNotExists: lambda req, exc: user_does_not_exists_response,
    exceptions.IncorrectPassword: lambda req, exc: incorrect_username_or_password_response,
    exceptions.IncorrectUsername: lambda req, exc: incorrect_username_or_password_response,
}
