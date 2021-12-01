import pytest
from geojson_pydantic import Point
from pydantic import BaseModel

from src.venue.domain.venue_repository import BasicVenueRepository


class VenueSample(BaseModel):
    name: str = 'MyVenue'
    description: str = 'A night club'
    province: str = 'Madrid'
    country: str = 'Spain'
    geolocation: Point = Point(type='Point', coordinates=[13, 14])
    owner_email: str = 'new_user@mail.es'


class PrivateSpotSample(BaseModel):
    name: str = 'Premium spot'
    description: str = 'The best private spot of the universe'
    spot_number: int = 1
    price: int = 100_00  # noqa: WPS303


@pytest.fixture
def private_spot_sample():
    return PrivateSpotSample()


@pytest.fixture
def venue_sample():
    return VenueSample()


@pytest.fixture
def venue_repository():
    return BasicVenueRepository()
