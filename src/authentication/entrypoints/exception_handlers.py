from typing import Callable
from typing import Type

from fastapi import Request
from fastapi import status
from fastapi.responses import JSONResponse

from src.authentication.domain import exceptions
from src.error_models import APIError

auth_exc_handlers: dict[Type[Exception], Callable[[Request | None, Exception | None], JSONResponse]] = {}

bearer_header = {'WWW-Authenticate': 'Bearer'}

UNAUTHORIZED = 201
unauthorized_response = JSONResponse(
    APIError(detail='Could not validate credentials', error_code=UNAUTHORIZED).dict(),
    status_code=status.HTTP_401_UNAUTHORIZED,
    headers=bearer_header,
)
auth_exc_handlers[exceptions.Unauthorized] = lambda req, exc: unauthorized_response


USER_ALREADY_REGISTERED = 202
user_already_registered_response = JSONResponse(
    APIError(detail='User already exists', error_code=USER_ALREADY_REGISTERED).dict(),
    status_code=status.HTTP_400_BAD_REQUEST,
)
auth_exc_handlers[exceptions.UserAlreadyRegistered] = lambda req, exc: user_already_registered_response


INCORRECT_USERNAME_OR_PASSWORD = 203
incorrect_username_or_password_response = JSONResponse(
    APIError(
        detail='Incorrect username or password',
        error_code=INCORRECT_USERNAME_OR_PASSWORD,
    ).dict(),
    status_code=status.HTTP_400_BAD_REQUEST,
    headers=bearer_header,
)
auth_exc_handlers[exceptions.IncorrectUsername] = lambda req, exc: incorrect_username_or_password_response
auth_exc_handlers[exceptions.IncorrectPassword] = lambda req, exc: incorrect_username_or_password_response


USER_DOES_NOT_EXIST = 204
user_does_not_exist_response = JSONResponse(
    APIError(detail='User does not exist', error_code=USER_DOES_NOT_EXIST).dict(),
    status_code=status.HTTP_400_BAD_REQUEST,
    headers=bearer_header,
)
auth_exc_handlers[exceptions.UserDoesNotExist] = lambda req, exc: user_does_not_exist_response


USER_EMAIL_NOT_VERIFIED = 205
user_email_not_verified = JSONResponse(
    APIError(detail='User email not verified', error_code=USER_EMAIL_NOT_VERIFIED).dict(),
    status_code=status.HTTP_401_UNAUTHORIZED,
    headers=bearer_header,
)
auth_exc_handlers[exceptions.UserEmailNotVerified] = lambda req, exc: user_email_not_verified


USER_WITHOT_PROFILE = 206
user_without_profile = JSONResponse(
    APIError(detail='User without profile', error_code=USER_WITHOT_PROFILE).dict(),
    status_code=status.HTTP_401_UNAUTHORIZED,
    headers=bearer_header,
)
auth_exc_handlers[exceptions.UserWithoutProfile] = lambda req, exc: user_without_profile
