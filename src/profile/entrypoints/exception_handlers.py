from typing import Callable
from typing import Type

from fastapi import Request
from fastapi import status
from fastapi.responses import JSONResponse

from src.error_models import APIError
from src.profile.domain import exceptions


profile_exc_handlers: dict[Type[Exception], Callable[[Request | None, Exception | None], JSONResponse]] = {}


PROFILE_ALREADY_INITIALIZED = 101
profile_already_initialized_response = JSONResponse(
    APIError(detail='User profile already initialized', error_code=PROFILE_ALREADY_INITIALIZED).dict(),
    status_code=status.HTTP_400_BAD_REQUEST,
)
profile_exc_handlers[exceptions.ProfileAlreadyInitialized] = lambda req, exc: profile_already_initialized_response


PROFILE_DOES_NOT_EXIST = 102
profile_does_not_exist_response = JSONResponse(
    APIError(detail='User profile does not exist', error_code=PROFILE_DOES_NOT_EXIST).dict(),
    status_code=status.HTTP_400_BAD_REQUEST,
    headers={'WWW-Authenticate': 'Bearer'},
)
profile_exc_handlers[exceptions.ProfileDoesNotExist] = lambda req, exc: profile_does_not_exist_response
