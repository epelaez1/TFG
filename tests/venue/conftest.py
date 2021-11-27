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


@pytest.fixture
def venue_sample():
    return VenueSample()


@pytest.fixture
def venue_repository():
    return BasicVenueRepository()
