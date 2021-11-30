import pytest
from bson import ObjectId

from src.venue import venue_services
from src.venue.domain import exceptions
from src.venue.domain.venue_repository import VenueRepository
from tests.venue.conftest import VenueSample


def test_register_venue(venue_sample: VenueSample, venue_repository: VenueRepository):
    venue_id: ObjectId = venue_services.register_venue(**venue_sample.dict(), venue_repository=venue_repository)
    assert venue_repository.has(id_=venue_id)


def test_get_venue(venue_sample: VenueSample, venue_repository: VenueRepository):
    venue_id: ObjectId = venue_services.register_venue(**venue_sample.dict(), venue_repository=venue_repository)
    venue_services.get_venue(str(venue_id), venue_repository=venue_repository)


def test_get_inexistent_venue(venue_repository: VenueRepository):
    with pytest.raises(exceptions.VenueDoesNotExist):
        venue_services.get_venue(str(ObjectId()), venue_repository=venue_repository)
