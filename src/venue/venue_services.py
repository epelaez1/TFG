from geojson_pydantic import Point

from src.venue.domain import exceptions
from src.venue.domain.venue import PrivateSpot
from src.venue.domain.venue import Venue
from src.venue.domain.venue_repository import VenueRepository


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
    venue_repository.add(venue=venue)
    return str(venue.id)


def get_venue(id_: str, venue_repository: VenueRepository) -> Venue:
    return venue_repository.get(id_=id_)


def add_private_spot(  # noqa: WPS211 Too many arguments
    venue_id: str,
    author_email: str,
    spot_number: int,
    price: int,
    name: str | None,
    description: str | None,
    venue_repository: VenueRepository,
) -> None:
    venue = venue_repository.get(id_=venue_id)
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

    venue_repository.add_private_spot(id_=venue_id, private_spot=private_spot)
