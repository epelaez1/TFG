import json

import pytest
from fastapi import status
from fastapi.responses import JSONResponse

from src.error_models import APIError
from src.venue.domain import exceptions
from src.venue.entrypoints import exception_handlers


@pytest.mark.parametrize(('exception', 'status_code', 'error_code'), [
    (
        exceptions.VenueDoesNotExist,
        status.HTTP_404_NOT_FOUND,
        exception_handlers.VENUE_DOES_NOT_EXIST,
    ),
    (
        exceptions.AuthorIsNotTheOwner,
        status.HTTP_401_UNAUTHORIZED,
        exception_handlers.AUTHOR_IS_NOT_THE_OWNER,
    ),
    (
        exceptions.PrivateSpotNumberAlreadyAssigned,
        status.HTTP_400_BAD_REQUEST,
        exception_handlers.PRIVATE_SPOT_NUMBER_ALREADY_ASSIGNED,
    ),
    (
        exceptions.SocialEventDoesNotExist,
        status.HTTP_404_NOT_FOUND,
        exception_handlers.SOCIAL_EVENT_DOES_NOT_EXIST,
    ),
    (
        exceptions.EmployeeCodeAlreadyInUse,
        status.HTTP_400_BAD_REQUEST,
        exception_handlers.EMPLOYEE_CODE_ALREADY_IN_USE,
    ),
    (
        exceptions.PrivateSpotNotFound,
        status.HTTP_404_NOT_FOUND,
        exception_handlers.PRIVATE_SPOT_NOT_FOUND,
    ),
    (
        exceptions.SpotOfferAlreadyExists,
        status.HTTP_400_BAD_REQUEST,
        exception_handlers.SPOT_OFFER_ALREADY_EXISTS,
    ),
    (
        exceptions.PrivateSpotOfferDoesNotExist,
        status.HTTP_404_NOT_FOUND,
        exception_handlers.PRIVATE_SPOT_OFFER_DOES_NOT_EXIST,
    ),
    (
        exceptions.PrivateSpotIsNotAvailable,
        status.HTTP_400_BAD_REQUEST,
        exception_handlers.PRIVATE_SPOT_IS_NOT_AVAILABLE,
    ),
    (
        exceptions.UserIsNotInsideTheSocialEvent,
        status.HTTP_400_BAD_REQUEST,
        exception_handlers.USER_HAS_NEVER_ACCESSED_THE_SOCIAL_EVENT,
    ),
])
def test_auth_exceptions_are_handled(exception, status_code, error_code):
    assert exception in exception_handlers.venue_exc_handlers
    response: JSONResponse = exception_handlers.venue_exc_handlers[exception](None, None)
    error_details = APIError(**json.loads(response.body))
    assert response.status_code == status_code
    assert error_details.error_code == error_code
