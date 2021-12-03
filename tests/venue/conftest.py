from datetime import datetime
from datetime import timedelta

import pytest
from bson import ObjectId
from geojson_pydantic import Point
from pydantic import BaseModel
from pydantic import Field

from src.venue.domain.entities.social_event import PrivateSpotOffer
from src.venue.domain.entities.social_event import SocialEvent
from src.venue.domain.entities.venue import PrivateSpot
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
    spot_number: int = 55
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
    private_spot = PrivateSpot(
        spot_number=1,
        price=200_00,  # noqa: WPS432, WPS303  Magic number and underscored number
        name='Best spot',
        description='Near the show',
    )
    venue = Venue(
        _id=registered_venue_id,
        **{
            **venue_sample.dict(),
            'owner_email': registered_owner,
        },
    )
    venue.private_spots = {private_spot}
    return venue


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


class EmployeeListSample(BaseModel):
    employee_name: str = 'Bob'
    code: str = 'QWERTY'


@pytest.fixture
def employee_list_sample() -> EmployeeListSample:
    return EmployeeListSample()


@pytest.fixture
def registered_social_event_id() -> str:
    return '61a964bd62e7d5b769ffd163'


@pytest.fixture
def registered_social_event(
    registered_owner: str,
    registered_social_event_id: str,
    registered_venue: Venue,
) -> SocialEvent:
    social_event_data = {
        **SocialEventSample().dict(),
        'venue_id': str(registered_venue.id),
    }
    private_spot_offers = {
        PrivateSpotOffer(**private_spot.dict())
        for private_spot in registered_venue.private_spots
    }
    return SocialEvent(
        _id=registered_social_event_id,
        owner_email=registered_owner,
        private_spot_offers=private_spot_offers,
        **social_event_data,
    )


@pytest.fixture
def venue_repository(
    registered_venue: Venue,
    registered_social_event: SocialEvent,
) -> VenueRepository:
    repo = BasicVenueRepository()
    repo.add_venue(registered_venue)
    repo.add_social_event(registered_social_event)
    return repo
