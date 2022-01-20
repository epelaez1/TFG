from fastapi import APIRouter
from fastapi import Depends
from fastapi import status

from src.dependencies import authorized_user_email
from src.dependencies import repositories
from src.venue import services
from src.venue.domain.entities.social_event import SocialEvent
from src.venue.domain.entities.venue import Venue
from src.venue.entrypoints import models

venue_router: APIRouter = APIRouter(
    prefix='/venue',
)


@venue_router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=models.Venue,
    name='venue:create',
)
async def create_profile(
    venue: models.NewVenue,
    email: str = Depends(authorized_user_email),  # noqa: WPS204
) -> Venue:
    venue_id = services.register_venue(
        **venue.dict(),
        owner_email=email,
        venue_repository=repositories.venue_repository,
    )
    return services.get_venue(venue_id, venue_repository=repositories.venue_repository)


@venue_router.get(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=models.PublicVenue,
    name='venue:create',
)
async def get_venue(
    venue_id: str,
) -> Venue:
    return services.get_venue(venue_id, venue_repository=repositories.venue_repository)


@venue_router.post(
    '/private_spot',
    status_code=status.HTTP_200_OK,
    name='venue:add-private-spot',
)
async def add_private_spot(
    private_spot: models.PrivateSpot,
    venue_id: str,
    email: str = Depends(authorized_user_email),
) -> None:
    return services.add_private_spot(
        venue_id=venue_id,
        author_email=email,
        venue_repository=repositories.venue_repository,
        **private_spot.dict(),
    )


@venue_router.post(
    '/social_event',
    status_code=status.HTTP_201_CREATED,
    response_model=models.SocialEvent,
    name='venue:create-social-event',
)
async def create_social_event(
    venue_id: str,
    social_event: models.NewSocialEvent,
    email: str = Depends(authorized_user_email),
) -> SocialEvent:
    social_event_id = services.create_social_event(
        author_email=email,
        venue_id=venue_id,
        venue_repository=repositories.venue_repository,
        **social_event.dict(),
    )
    return services.get_social_event(
        author_email=email,
        social_event_id=social_event_id,
        venue_repository=repositories.venue_repository,
    )


@venue_router.post(
    '/social_event/employee_list',
    status_code=status.HTTP_200_OK,
    name='venue:add-employee-list-to-social-event',
)
async def add_employee_list_to_social_event(
    social_event_id: str,
    employee_list: models.PublicEmployeeList,
    email: str = Depends(authorized_user_email),
) -> None:
    services.add_employee_list_to_social_event(
        author_email=email,
        social_event_id=social_event_id,
        venue_repository=repositories.venue_repository,
        **employee_list.dict(),
    )


@venue_router.get(
    '/all',
    status_code=status.HTTP_200_OK,
    response_model=list[models.PublicVenue],
    name='venue:all',
)
async def get_all_venues() -> list[Venue]:
    return services.get_all_venues(venue_repository=repositories.venue_repository)


@venue_router.get(
    '/social_event/all',
    status_code=status.HTTP_200_OK,
    response_model=list[models.PublicSocialEvent],
    name='venue:all-social-events',
)
async def get_all_social_events() -> list[SocialEvent]:
    return services.get_all_social_events(venue_repository=repositories.venue_repository)


@venue_router.get(
    '/social_event/by_venue',
    status_code=status.HTTP_200_OK,
    response_model=list[models.PublicSocialEvent],
    name='venue:all-social-events-of-venue',
)
async def get_social_event_of_venue(
    venue_id: str,
) -> list[SocialEvent]:
    return services.get_social_events_of_venue(venue_id=venue_id, venue_repository=repositories.venue_repository)


@venue_router.post(
    '/social_event/add_spot_offer',
    status_code=status.HTTP_200_OK,
    name='venue:add-spot-offer-to-social-event',
)
async def add_spot_offer_to_social_event(
    spot_number: int,
    social_event_id: str,
    email: str = Depends(authorized_user_email),
) -> None:
    return services.add_private_spot_offer_to_social_event(
        social_event_id=social_event_id,
        author_email=email,
        spot_number=spot_number,
        venue_repository=repositories.venue_repository,
    )


@venue_router.post(
    '/social_event/reserve',
    status_code=status.HTTP_200_OK,
    name='venue:reserve',
)
async def reserve_spot(
    spot_number: int,
    social_event_id: str,
    email: str = Depends(authorized_user_email),
) -> None:
    return services.reserve_spot(
        author_email=email,
        spot_number=spot_number,
        social_event_id=social_event_id,
        venue_repository=repositories.venue_repository,
    )


@venue_router.post(
    '/social_event/join',
    status_code=status.HTTP_200_OK,
    name='venue:join-event',
)
async def join_social_event(
    employee_code: str,
    social_event_id: str,
    email: str = Depends(authorized_user_email),
) -> None:
    return services.join_social_event(
        author_email=email,
        employee_code=employee_code,
        social_event_id=social_event_id,
        venue_repository=repositories.venue_repository,
    )


@venue_router.post(
    '/social_event/access',
    status_code=status.HTTP_200_OK,
    name='venue:access',
)
async def access_social_event(
    social_event_id: str,
    email: str = Depends(authorized_user_email),
) -> None:
    return services.access_social_event(
        author_email=email,
        social_event_id=social_event_id,
        venue_repository=repositories.venue_repository,
    )


@venue_router.post(
    '/social_event/leave',
    status_code=status.HTTP_200_OK,
    name='venue:leave',
)
async def leave_social_event(
    social_event_id: str,
    email: str = Depends(authorized_user_email),
) -> None:
    return services.leave_social_event(
        author_email=email,
        social_event_id=social_event_id,
        venue_repository=repositories.venue_repository,
    )
