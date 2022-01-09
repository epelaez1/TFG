from typing import Callable
from typing import Type

from fastapi import Request
from fastapi import status
from fastapi.responses import JSONResponse

from src.error_models import APIError
from src.venue.domain import exceptions


venue_exc_handlers: dict[Type[Exception], Callable[[Request | None, Exception | None], JSONResponse]] = {}


VENUE_DOES_NOT_EXIST = 301
venue_does_not_exist_response = JSONResponse(
    APIError(detail='Venue does not exist', error_code=VENUE_DOES_NOT_EXIST).dict(),
    status_code=status.HTTP_404_NOT_FOUND,
)
venue_exc_handlers[exceptions.VenueDoesNotExist] = lambda req, exc: venue_does_not_exist_response

AUTHOR_IS_NOT_THE_OWNER = 302
author_is_not_the_owner = JSONResponse(
    APIError(detail='Not enough permissions', error_code=AUTHOR_IS_NOT_THE_OWNER).dict(),
    status_code=status.HTTP_401_UNAUTHORIZED,
)
venue_exc_handlers[exceptions.AuthorIsNotTheOwner] = lambda req, exc: author_is_not_the_owner

PRIVATE_SPOT_NUMBER_ALREADY_ASSIGNED = 303
private_spot_already_assigned = JSONResponse(
    APIError(detail='The spot already exist in the venue', error_code=PRIVATE_SPOT_NUMBER_ALREADY_ASSIGNED).dict(),
    status_code=status.HTTP_400_BAD_REQUEST,
)
venue_exc_handlers[exceptions.PrivateSpotNumberAlreadyAssigned] = lambda req, exc: private_spot_already_assigned

SOCIAL_EVENT_DOES_NOT_EXIST = 304
social_event_does_not_exist = JSONResponse(
    APIError(detail='There is no social event with that id', error_code=SOCIAL_EVENT_DOES_NOT_EXIST).dict(),
    status_code=status.HTTP_404_NOT_FOUND,
)
venue_exc_handlers[exceptions.SocialEventDoesNotExist] = lambda req, exc: social_event_does_not_exist

EMPLOYEE_CODE_ALREADY_IN_USE = 305
employee_code_already_in_use = JSONResponse(
    APIError(detail='Employee code already in use', error_code=EMPLOYEE_CODE_ALREADY_IN_USE).dict(),
    status_code=status.HTTP_400_BAD_REQUEST,
)
venue_exc_handlers[exceptions.EmployeeCodeAlreadyInUse] = lambda req, exc: employee_code_already_in_use

PRIVATE_SPOT_NOT_FOUND = 306
private_spot_not_found = JSONResponse(
    APIError(detail='Private spot not found', error_code=PRIVATE_SPOT_NOT_FOUND).dict(),
    status_code=status.HTTP_404_NOT_FOUND,
)
venue_exc_handlers[exceptions.PrivateSpotNotFound] = lambda req, exc: private_spot_not_found

SPOT_OFFER_ALREADY_EXISTS = 307
spot_offer_already_exists = JSONResponse(
    APIError(detail='Private spot offer already exists', error_code=SPOT_OFFER_ALREADY_EXISTS).dict(),
    status_code=status.HTTP_400_BAD_REQUEST,
)
venue_exc_handlers[exceptions.SpotOfferAlreadyExists] = lambda req, exc: spot_offer_already_exists

PRIVATE_SPOT_OFFER_DOES_NOT_EXIST = 308
private_spot_offer_not_found = JSONResponse(
    APIError(detail='Private spot offer not found', error_code=PRIVATE_SPOT_OFFER_DOES_NOT_EXIST).dict(),
    status_code=status.HTTP_404_NOT_FOUND,
)
venue_exc_handlers[exceptions.PrivateSpotOfferDoesNotExist] = lambda req, exc: private_spot_offer_not_found

PRIVATE_SPOT_IS_NOT_AVAILABLE = 309
private_spot_not_available = JSONResponse(
    APIError(detail='Private spot offer not available', error_code=PRIVATE_SPOT_IS_NOT_AVAILABLE).dict(),
    status_code=status.HTTP_400_BAD_REQUEST,
)
venue_exc_handlers[exceptions.PrivateSpotIsNotAvailable] = lambda req, exc: private_spot_not_available

USER_HAS_NEVER_ACCESSED_THE_SOCIAL_EVENT = 310
user_is_not_inside = JSONResponse(
    APIError(detail='User has never accessed the event', error_code=USER_HAS_NEVER_ACCESSED_THE_SOCIAL_EVENT).dict(),
    status_code=status.HTTP_400_BAD_REQUEST,
)
venue_exc_handlers[exceptions.UserIsNotInsideTheSocialEvent] = lambda req, exc: user_is_not_inside
