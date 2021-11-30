from geojson_pydantic import Point

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
    return venue.id


def get_venue(id_: str, venue_repository: VenueRepository) -> Venue:
    return venue_repository.get(id_=id_)
