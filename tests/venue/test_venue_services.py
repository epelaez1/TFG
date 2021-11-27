from bson import ObjectId

from src.venue import venue_services
from src.venue.domain.venue_repository import VenueRepository
from tests.venue.conftest import VenueSample


def test_register_venue(venue_sample: VenueSample, venue_repository: VenueRepository):
    venue_id: ObjectId = venue_services.register_venue(**venue_sample.dict(), venue_repository=venue_repository)
    assert venue_repository.has(id_=venue_id)
