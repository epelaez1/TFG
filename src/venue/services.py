from datetime import datetime

from geojson_pydantic import Point

from src.venue.domain import exceptions
from src.venue.domain.entities.social_event import PrivateSpotOffer
from src.venue.domain.entities.social_event import SocialEvent
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

    venue.add_private_spot(
        spot_number=spot_number,
        name=name,
        description=description,
        price=price,
    )

    venue_repository.update_venue(venue_id=venue_id, new_venue=venue)


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
    private_spot_offers = {
        PrivateSpotOffer(**private_spot.dict())
        for private_spot in venue.private_spots
    }
    social_event = SocialEvent(
        owner_email=author_email,
        venue_id=venue_id,
        name=name,
        description=description,
        start_date=start_date,
        end_date=end_date,
        private_spot_offers=private_spot_offers,
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

    social_event.add_employee_list(code, employee_name)
    venue_repository.update_social_event(social_event_id=social_event_id, new_social_event=social_event)


def get_all_venues(venue_repository: VenueRepository) -> list[Venue]:
    return venue_repository.get_all_venues()


def get_all_social_events(venue_repository: VenueRepository) -> list[SocialEvent]:
    return venue_repository.get_all_social_events()


def get_social_events_of_venue(venue_id: str, venue_repository: VenueRepository) -> list[SocialEvent]:
    return venue_repository.get_social_events_of_venue(venue_id=venue_id)


def add_private_spot_offer_to_social_event(
    social_event_id: str,
    author_email: str,
    spot_number: int,
    venue_repository: VenueRepository,
) -> None:

    social_event = venue_repository.get_social_event(
        social_event_id=social_event_id,
    )
    venue = venue_repository.get_venue(social_event.venue_id)

    if author_email != venue.owner_email or author_email != social_event.owner_email:
        raise exceptions.AuthorIsNotTheOwner()

    venue.add_private_spot_offer_to_social_event(
        social_event=social_event,
        spot_number=spot_number,
    )
    venue_repository.update_social_event(
        social_event_id=social_event_id,
        new_social_event=social_event,
    )


def reserve_spot(
    author_email: str,
    spot_number: int,
    social_event_id: str,
    venue_repository: VenueRepository,
) -> None:
    social_event = venue_repository.get_social_event(
        social_event_id=social_event_id,
    )

    social_event.reserve_spot(author_email=author_email, spot_number=spot_number)
    venue_repository.update_social_event(social_event_id, social_event)


def join_social_event(
    author_email: str,
    employee_code: str,
    social_event_id: str,
    venue_repository: VenueRepository,
) -> None:
    social_event = venue_repository.get_social_event(
        social_event_id=social_event_id,
    )

    social_event.join(author_email, employee_code)
    venue_repository.update_social_event(social_event_id, social_event)


def access_social_event(
    author_email: str,
    social_event_id: str,
    venue_repository: VenueRepository,
) -> None:
    social_event = venue_repository.get_social_event(
        social_event_id=social_event_id,
    )
    social_event.access_social_event(user_email=author_email)
    venue_repository.update_social_event(social_event_id, social_event)


def leave_social_event(
    author_email: str,
    social_event_id: str,
    venue_repository: VenueRepository,
) -> None:
    social_event = venue_repository.get_social_event(
        social_event_id=social_event_id,
    )
    social_event.leave_social_event(user_email=author_email)
    venue_repository.update_social_event(social_event_id, social_event)
