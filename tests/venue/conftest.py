from datetime import datetime
from datetime import timedelta

import pytest
from bson import ObjectId
from geojson_pydantic import Point
from pydantic import BaseModel
from pydantic import Field

from src.resources.pydantic_types.object_id import PyObjectId
from src.venue.domain.repository import BasicVenueRepository


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


def tomorrow() -> datetime:
    return datetime.utcnow() + timedelta(days=1)


def object_id_str() -> str:
    return str(ObjectId())


class SocialEventSample(BaseModel):
    venue_id: PyObjectId = Field(default_factory=object_id_str)
    name: str = 'Social Event'
    description: str = 'A great show'
    start_date: datetime = Field(default_factory=datetime.utcnow)
    end_date: datetime = Field(default_factory=tomorrow)
    author_email: str = 'new_user@mail.es'


@pytest.fixture
def social_event_sample() -> SocialEventSample:
    return SocialEventSample()
