from datetime import datetime
from datetime import timedelta

import pytest
from bson import ObjectId
from geojson_pydantic import Point
from pydantic import BaseModel
from pydantic import Field

from src.venue.domain.entities.venue import Venue
from src.venue.domain.repository import BasicVenueRepository
from src.venue.domain.repository import VenueRepository


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
def registered_owner() -> str:
    return 'owner@mail.es'


@pytest.fixture
def registered_venue_id() -> str:
    return '61a9389558b8fdc0921ed04a'


@pytest.fixture
def registered_venue(
    registered_owner: str,
    registered_venue_id: str,
    venue_sample: VenueSample,
) -> Venue:
    return Venue(
        _id=registered_venue_id,
        **{
            **venue_sample.dict(),
            'owner_email': registered_owner,
        },
    )


@pytest.fixture
def venue_repository(registered_venue: Venue) -> VenueRepository:
    repo = BasicVenueRepository()
    repo.add_venue(registered_venue)
    return repo


def tomorrow() -> datetime:
    return datetime.utcnow() + timedelta(days=1)


def object_id_str() -> str:
    return str(ObjectId())


class SocialEventSample(BaseModel):
    venue_id: str = Field(default_factory=object_id_str)
    name: str = 'Social Event'
    description: str = 'A great show'
    start_date: datetime = Field(default_factory=datetime.utcnow)
    end_date: datetime = Field(default_factory=tomorrow)


@pytest.fixture
def social_event_sample() -> SocialEventSample:
    return SocialEventSample()
