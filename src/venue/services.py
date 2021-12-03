from datetime import datetime

from geojson_pydantic import Point

from src.venue.domain import exceptions
from src.venue.domain.entities.social_event import EmployeeList
from src.venue.domain.entities.social_event import SocialEvent
from src.venue.domain.entities.venue import PrivateSpot
from src.venue.domain.entities.venue import Venue
from src.venue.domain.repository import VenueRepository


def register_venue(  # noqa: WPS211
    name: str,
    description: str,
    province: str,
    country: str,
    geolocation: Point,
    owner_email: str,
    venue_repository: VenueRepository,
) -> str:
    venue = Venue(
        name=name,
        description=description,
        province=province,
        country=country,
        geolocation=geolocation,
        owner_email=owner_email,
    )
    venue_repository.add_venue(venue=venue)
    return str(venue.id)


def get_venue(venue_id: str, venue_repository: VenueRepository) -> Venue:
    return venue_repository.get_venue(venue_id=venue_id)


def add_private_spot(  # noqa: WPS211 Too many arguments
    venue_id: str,
    author_email: str,
    spot_number: int,
    price: int,
    name: str | None,
    description: str | None,
    venue_repository: VenueRepository,
) -> None:
    venue = venue_repository.get_venue(venue_id=venue_id)
    if venue.owner_email != author_email:
        raise exceptions.AuthorIsNotTheOwner()

    if spot_number in venue.private_spot_numbers:
        raise exceptions.PrivateSpotNumberAlreadyAssigned()

    private_spot = PrivateSpot(
        spot_number=spot_number,
        name=name,
        description=description,
        price=price,
    )

    venue_repository.add_private_spot(venue_id=venue_id, private_spot=private_spot)


def create_social_event(  # noqa: WPS211 Too many arguments
    author_email: str,
    venue_id: str,
    name: str,
    description: str,
    start_date: datetime,
    end_date: datetime,
    venue_repository: VenueRepository,
) -> str:

    venue = venue_repository.get_venue(venue_id)
    if author_email != venue.owner_email:
        raise exceptions.AuthorIsNotTheOwner()

    social_event = SocialEvent(
        owner_email=author_email,
        venue_id=venue_id,
        name=name,
        description=description,
        start_date=start_date,
        end_date=end_date,
    )
    venue_repository.add_social_event(social_event)
    return str(social_event.id)


def get_social_event(author_email: str, social_event_id: str, venue_repository: VenueRepository) -> SocialEvent:
    social_event = venue_repository.get_social_event(social_event_id)
    if social_event.owner_email != author_email:
        raise exceptions.AuthorIsNotTheOwner()
    return social_event


def add_employee_list_to_social_event(
    author_email: str,
    employee_name: str,
    code: str,
    social_event_id: str,
    venue_repository: VenueRepository,
) -> None:

    social_event = venue_repository.get_social_event(social_event_id=social_event_id)
    if author_email != social_event.owner_email:
        raise exceptions.AuthorIsNotTheOwner()

    if code in social_event.employee_lists:
        raise exceptions.EmployeeCodeAlreadyInUse()

    employee_list = EmployeeList(code=code, employee_name=employee_name)
    venue_repository.add_employee_list_to_social_event(social_event_id=social_event_id, employee_list=employee_list)
