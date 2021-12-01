import pytest
from bson import ObjectId

from src.venue import venue_services
from src.venue.domain import exceptions
from src.venue.domain.venue_repository import VenueRepository
from tests.venue.conftest import PrivateSpotSample
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


def test_add_new_private_spot(
    private_spot_sample: PrivateSpotSample,
    venue_sample: VenueSample,
    venue_repository: VenueRepository,
):
    venue_id: ObjectId = venue_services.register_venue(**venue_sample.dict(), venue_repository=venue_repository)
    venue_services.add_private_spot(
        venue_id=venue_id,
        author_email=venue_sample.owner_email,
        venue_repository=venue_repository,
        **private_spot_sample.dict(),
    )
    new_venue = venue_repository.get(id_=venue_id)
    assert private_spot_sample.spot_number in new_venue.private_spot_numbers
    created_spot = next(
        private_spot
        for private_spot in new_venue.private_spots
        if private_spot.spot_number == private_spot_sample.spot_number
    )
    assert ObjectId.is_valid(created_spot.id)
    assert created_spot.dict(by_alias=True) == {**private_spot_sample.dict(), '_id': created_spot.id}


def test_add_private_spot_with_number_in_use(
    private_spot_sample: PrivateSpotSample,
    venue_sample: VenueSample,
    venue_repository: VenueRepository,
):
    venue_id: ObjectId = venue_services.register_venue(**venue_sample.dict(), venue_repository=venue_repository)
    venue_services.add_private_spot(
        venue_id=venue_id,
        author_email=venue_sample.owner_email,
        venue_repository=venue_repository,
        **private_spot_sample.dict(),
    )
    with pytest.raises(exceptions.PrivateSpotNumberAlreadyAssigned):
        venue_services.add_private_spot(
            venue_id=venue_id,
            author_email=venue_sample.owner_email,
            venue_repository=venue_repository,
            **private_spot_sample.dict(),
        )


def test_not_owner_add_private_spot(
    private_spot_sample: PrivateSpotSample,
    venue_sample: VenueSample,
    venue_repository: VenueRepository,
):
    venue_id: ObjectId = venue_services.register_venue(**venue_sample.dict(), venue_repository=venue_repository)
    with pytest.raises(exceptions.AuthorIsNotTheOwner):
        venue_services.add_private_spot(
            venue_id=venue_id,
            author_email='not_the_owner@mail.es',
            venue_repository=venue_repository,
            **private_spot_sample.dict(),
        )


def test_add_private_spot_to_inexistent_venue(
    private_spot_sample: PrivateSpotSample,
    venue_repository: VenueRepository,
):
    with pytest.raises(exceptions.VenueDoesNotExist):
        venue_services.add_private_spot(
            venue_id=str(ObjectId()),
            author_email='some_email@mail.es',
            venue_repository=venue_repository,
            **private_spot_sample.dict(),
        )
