import pytest
from bson import ObjectId

from src.venue import services
from src.venue.domain import exceptions
from src.venue.domain.entities.venue import Venue
from src.venue.domain.repository import VenueRepository
from tests.venue.conftest import EmployeeListSample
from tests.venue.conftest import PrivateSpotSample
from tests.venue.conftest import SocialEventSample
from tests.venue.conftest import VenueSample


def test_register_venue(venue_sample: VenueSample, venue_repository: VenueRepository):
    venue_id: str = services.register_venue(
        **venue_sample.dict(),
        venue_repository=venue_repository,
    )
    assert venue_repository.has_venue(venue_id=venue_id)
    new_venue = venue_repository.get_venue(venue_id)
    assert venue_sample.dict().items() <= new_venue.dict().items()


def test_get_venue(registered_venue_id: str, venue_repository: VenueRepository):
    venue = services.get_venue(str(registered_venue_id), venue_repository=venue_repository)
    assert str(venue.id) == registered_venue_id


def test_get_inexistent_venue(venue_repository: VenueRepository):
    with pytest.raises(exceptions.VenueDoesNotExist):
        services.get_venue(str(ObjectId()), venue_repository=venue_repository)


def test_add_new_private_spot(
    registered_venue: Venue,
    private_spot_sample: PrivateSpotSample,
    venue_repository: VenueRepository,
):
    services.add_private_spot(
        venue_id=str(registered_venue.id),
        author_email=registered_venue.owner_email,
        venue_repository=venue_repository,
        **private_spot_sample.dict(),
    )
    new_venue = venue_repository.get_venue(venue_id=str(registered_venue.id))
    assert private_spot_sample.spot_number in new_venue.private_spot_numbers
    created_spot = next(
        private_spot
        for private_spot in new_venue.private_spots
        if private_spot.spot_number == private_spot_sample.spot_number
    )
    assert ObjectId.is_valid(created_spot.id)
    assert created_spot.dict(by_alias=True) == {**private_spot_sample.dict(), '_id': created_spot.id}


def test_add_private_spot_with_number_in_use(
    registered_venue: Venue,
    private_spot_sample: PrivateSpotSample,
    venue_repository: VenueRepository,
):
    services.add_private_spot(
        venue_id=str(registered_venue.id),
        author_email=registered_venue.owner_email,
        venue_repository=venue_repository,
        **private_spot_sample.dict(),
    )
    with pytest.raises(exceptions.PrivateSpotNumberAlreadyAssigned):
        services.add_private_spot(
            venue_id=str(registered_venue.id),
            author_email=registered_venue.owner_email,
            venue_repository=venue_repository,
            **private_spot_sample.dict(),
        )


def test_not_owner_add_private_spot(
    private_spot_sample: PrivateSpotSample,
    registered_venue_id: str,
    venue_repository: VenueRepository,
):
    with pytest.raises(exceptions.AuthorIsNotTheOwner):
        services.add_private_spot(
            venue_id=registered_venue_id,
            author_email='not_the_owner@mail.es',
            venue_repository=venue_repository,
            **private_spot_sample.dict(),
        )


def test_add_private_spot_to_inexistent_venue(
    private_spot_sample: PrivateSpotSample,
    venue_repository: VenueRepository,
):
    with pytest.raises(exceptions.VenueDoesNotExist):
        services.add_private_spot(
            venue_id=str(ObjectId()),
            author_email='some_email@mail.es',
            venue_repository=venue_repository,
            **private_spot_sample.dict(),
        )


def test_create_social_event(
    social_event_sample: SocialEventSample,
    registered_venue: Venue,
    venue_repository: VenueRepository,
):
    social_event_sample.venue_id = str(registered_venue.id)
    social_event_id = services.create_social_event(
        author_email=registered_venue.owner_email,
        **social_event_sample.dict(),
        venue_repository=venue_repository,
    )
    assert venue_repository.has_social_event(social_event_id=social_event_id)


def test_not_the_owner_create_social_event(
    social_event_sample: SocialEventSample,
    registered_venue_id: str,
    venue_repository: VenueRepository,
):
    social_event_sample.venue_id = registered_venue_id
    with pytest.raises(exceptions.AuthorIsNotTheOwner):
        services.create_social_event(
            author_email='not_the_owner@mail.es',
            **social_event_sample.dict(),
            venue_repository=venue_repository,
        )


def test_create_social_event_from_inexistent_venue(
    social_event_sample: SocialEventSample,
    venue_repository: VenueRepository,
):
    with pytest.raises(exceptions.VenueDoesNotExist):
        services.create_social_event(
            author_email='random@mail.es',
            **social_event_sample.dict(),
            venue_repository=venue_repository,
        )


def test_get_social_event(
    social_event_sample: SocialEventSample,
    registered_venue_id: str,
    registered_owner: str,
    venue_repository: VenueRepository,
):
    social_event_sample.venue_id = registered_venue_id
    social_event_id = services.create_social_event(
        **social_event_sample.dict(),
        author_email=registered_owner,
        venue_repository=venue_repository,
    )
    social_event = services.get_social_event(
        author_email=registered_owner,
        social_event_id=social_event_id,
        venue_repository=venue_repository,
    )

    assert str(social_event.id) == social_event_id
    assert social_event_sample.name == social_event.name
    assert social_event_sample.description == social_event.description
    assert social_event_sample.start_date == social_event.start_date
    assert social_event_sample.end_date == social_event.end_date


def test_not_the_owner_get_social_event(
    social_event_sample: SocialEventSample,
    registered_venue_id: str,
    registered_owner: str,
    venue_repository: VenueRepository,
):
    social_event_sample.venue_id = registered_venue_id
    social_event_id = services.create_social_event(
        author_email=registered_owner,
        **social_event_sample.dict(),
        venue_repository=venue_repository,
    )
    with pytest.raises(exceptions.AuthorIsNotTheOwner):
        services.get_social_event(
            author_email='not_the_owner@mail.es',
            social_event_id=social_event_id,
            venue_repository=venue_repository,
        )


def test_get_inexistent_social_event(
    venue_repository: VenueRepository,
):
    with pytest.raises(exceptions.SocialEventDoesNotExist):
        venue_repository.get_social_event(str(ObjectId()))


def test_add_employee_list_to_social_event(
    employee_list_sample: EmployeeListSample,
    registered_social_event_id: str,
    registered_owner: str,
    venue_repository: VenueRepository,
):
    services.add_employee_list_to_social_event(
        author_email=registered_owner,
        employee_name=employee_list_sample.employee_name,
        code=employee_list_sample.code,
        social_event_id=registered_social_event_id,
        venue_repository=venue_repository,
    )
    social_event = venue_repository.get_social_event(registered_social_event_id)
    employee_list = next(elem for elem in social_event.employee_lists if elem.code == employee_list_sample.code)
    assert employee_list
    assert employee_list_sample.dict().items() <= employee_list.dict().items()


def test_add_employee_list_to_inexistent_social_event(
    employee_list_sample: EmployeeListSample,
    registered_owner: str,
    venue_repository: VenueRepository,
):

    with pytest.raises(exceptions.SocialEventDoesNotExist):
        services.add_employee_list_to_social_event(
            author_email=registered_owner,
            employee_name=employee_list_sample.employee_name,
            code=employee_list_sample.code,
            social_event_id=ObjectId(),
            venue_repository=venue_repository,
        )


def test_not_the_owner_add_employee_list(
    employee_list_sample: EmployeeListSample,
    registered_social_event_id: str,
    venue_repository: VenueRepository,
):
    with pytest.raises(exceptions.AuthorIsNotTheOwner):
        services.add_employee_list_to_social_event(
            author_email='not_owner@mail.es',
            employee_name=employee_list_sample.employee_name,
            code=employee_list_sample.code,
            social_event_id=registered_social_event_id,
            venue_repository=venue_repository,
        )


def test_add_employee_list_with_repeated_code(
    employee_list_sample: EmployeeListSample,
    registered_social_event_id: str,
    registered_owner: str,
    venue_repository: VenueRepository,
):
    services.add_employee_list_to_social_event(
        author_email=registered_owner,
        employee_name=employee_list_sample.employee_name,
        code=employee_list_sample.code,
        social_event_id=registered_social_event_id,
        venue_repository=venue_repository,
    )

    with pytest.raises(exceptions.EmployeeCodeAlreadyInUse):
        services.add_employee_list_to_social_event(
            author_email=registered_owner,
            employee_name=employee_list_sample.employee_name,
            code=employee_list_sample.code,
            social_event_id=registered_social_event_id,
            venue_repository=venue_repository,
        )
