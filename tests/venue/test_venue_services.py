import pytest
from bson import ObjectId

from src.venue import services
from src.venue.domain import exceptions
from src.venue.domain.entities.social_event import PrivateSpotOffer
from src.venue.domain.entities.social_event import SocialEvent
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


def test_get_inexistent_venue(venue_repository: VenueRepository, random_id: str):
    with pytest.raises(exceptions.VenueDoesNotExist):
        services.get_venue(random_id, venue_repository=venue_repository)


def test_add_new_private_spot(
    registered_venue: Venue,
    private_spot_sample: PrivateSpotSample,
    venue_repository: VenueRepository,
):
    services.add_private_spot(
        venue_id=registered_venue.id_str,
        author_email=registered_venue.owner_email,
        venue_repository=venue_repository,
        **private_spot_sample.dict(),
    )
    venue = venue_repository.get_venue(venue_id=registered_venue.id_str)
    created_spot = venue.private_spots[private_spot_sample.spot_number]
    assert created_spot.dict() == private_spot_sample.dict()


def test_add_private_spot_with_number_in_use(
    registered_venue: Venue,
    private_spot_sample: PrivateSpotSample,
    venue_repository: VenueRepository,
):
    services.add_private_spot(
        venue_id=registered_venue.id_str,
        author_email=registered_venue.owner_email,
        venue_repository=venue_repository,
        **private_spot_sample.dict(),
    )
    with pytest.raises(exceptions.PrivateSpotNumberAlreadyAssigned):
        services.add_private_spot(
            venue_id=registered_venue.id_str,
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
    random_id: str,
    private_spot_sample: PrivateSpotSample,
    venue_repository: VenueRepository,
):
    with pytest.raises(exceptions.VenueDoesNotExist):
        services.add_private_spot(
            venue_id=random_id,
            author_email='some_email@mail.es',
            venue_repository=venue_repository,
            **private_spot_sample.dict(),
        )


def test_create_social_event(
    social_event_sample: SocialEventSample,
    registered_venue: Venue,
    venue_repository: VenueRepository,
):
    social_event_sample.venue_id = registered_venue.id_str
    social_event_id = services.create_social_event(
        author_email=registered_venue.owner_email,
        **social_event_sample.dict(),
        venue_repository=venue_repository,
    )
    assert venue_repository.has_social_event(social_event_id=social_event_id)
    social_event = venue_repository.get_social_event(social_event_id)
    assert len(registered_venue.private_spots)
    assert len(registered_venue.private_spots) == len(social_event.private_spot_offers)
    for private_spot in registered_venue.private_spots.values():
        private_spot_offer = PrivateSpotOffer(**private_spot.dict())
        assert private_spot_offer in social_event.private_spot_offers


def test_not_the_owner_create_social_event(
    social_event_sample: SocialEventSample,
    registered_venue_id: str,
    venue_repository: VenueRepository,
):
    social_event_sample.venue_id = registered_venue_id
    with pytest.raises(exceptions.AuthorIsNotTheOwner):
        services.create_social_event(
            author_email='not_the_owner@mail.org',
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
    random_id: str,
):
    with pytest.raises(exceptions.SocialEventDoesNotExist):
        venue_repository.get_social_event(random_id)


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
    employee_list = social_event.employee_lists[employee_list_sample.code]
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


def test_get_all_venues(
    venue_sample: VenueSample,
    venue_repository: VenueRepository,
):
    venue_id: str = services.register_venue(
        **venue_sample.dict(),
        venue_repository=venue_repository,
    )
    new_venue = venue_repository.get_venue(venue_id)
    venues = services.get_all_venues(venue_repository=venue_repository)
    assert bool(venues)
    assert new_venue in venues


def test_get_all_social_events(
    social_event_sample: SocialEventSample,
    venue_sample: VenueSample,
    registered_venue: Venue,
    venue_repository: VenueRepository,
):
    # First social event
    social_event_sample.venue_id = registered_venue.id_str
    social_event_id = services.create_social_event(
        author_email=registered_venue.owner_email,
        **social_event_sample.dict(),
        venue_repository=venue_repository,
    )
    # Second social event
    new_venue_id: str = services.register_venue(
        **venue_sample.dict(),
        venue_repository=venue_repository,
    )
    social_event_sample.venue_id = str(new_venue_id)
    second_social_event_id = services.create_social_event(
        author_email=venue_sample.owner_email,
        **social_event_sample.dict(),
        venue_repository=venue_repository,
    )
    social_events = services.get_all_social_events(venue_repository=venue_repository)
    social_event_ids = [str(social_event.id) for social_event in social_events]
    assert bool(social_events)
    assert social_event_id in social_event_ids
    assert second_social_event_id in social_event_ids


def test_get_social_events_of_venue(
    social_event_sample: SocialEventSample,
    venue_sample: VenueSample,
    registered_venue: Venue,
    venue_repository: VenueRepository,
):
    social_event_sample.venue_id = registered_venue.id_str
    social_event_id = services.create_social_event(
        author_email=registered_venue.owner_email,
        **social_event_sample.dict(),
        venue_repository=venue_repository,
    )
    # Second social event
    new_venue_id: str = services.register_venue(
        **venue_sample.dict(),
        venue_repository=venue_repository,
    )
    social_event_sample.venue_id = str(new_venue_id)
    second_social_event_id = services.create_social_event(
        author_email=venue_sample.owner_email,
        **social_event_sample.dict(),
        venue_repository=venue_repository,
    )
    social_events_of_venue = services.get_social_events_of_venue(
        venue_id=registered_venue.id_str,
        venue_repository=venue_repository,
    )
    social_event_ids = [str(social_event.id) for social_event in social_events_of_venue]
    assert social_events_of_venue
    assert str(social_event_id) in social_event_ids
    assert str(second_social_event_id) not in social_event_ids


def test_add_private_spot_offer_to_social_event(
    registered_social_event: SocialEvent,
    venue_repository: VenueRepository,
    private_spot_sample: PrivateSpotSample,
):
    services.add_private_spot(
        venue_id=str(registered_social_event.venue_id),
        author_email=registered_social_event.owner_email,
        venue_repository=venue_repository,
        **private_spot_sample.dict(),
    )
    services.add_private_spot_offer_to_social_event(
        social_event_id=registered_social_event.id_str,
        author_email=registered_social_event.owner_email,
        spot_number=private_spot_sample.spot_number,
        venue_repository=venue_repository,
    )
    social_event = services.get_social_event(
        author_email=registered_social_event.owner_email,
        social_event_id=registered_social_event.id_str,
        venue_repository=venue_repository,
    )
    private_spot_offer = next(
        (
            spot
            for spot in social_event.private_spot_offers
            if spot.spot_number == private_spot_sample.spot_number
        ),
        None,
    )
    assert private_spot_offer is not None
    assert private_spot_offer.price == private_spot_sample.price
    assert private_spot_offer.available
    assert private_spot_offer.buyer_email is None
    assert not private_spot_offer.users_list


def test_not_the_owner_adds_a_private_spot_offer_to_social_event(
    registered_social_event: SocialEvent,
    venue_repository: VenueRepository,
    private_spot_sample: PrivateSpotSample,
):
    not_the_owner_email = 'not_the_owner@mail.com'
    services.add_private_spot(
        venue_id=str(registered_social_event.venue_id),
        author_email=registered_social_event.owner_email,
        venue_repository=venue_repository,
        **private_spot_sample.dict(),
    )
    with pytest.raises(exceptions.AuthorIsNotTheOwner):
        services.add_private_spot_offer_to_social_event(
            social_event_id=registered_social_event.id_str,
            author_email=not_the_owner_email,
            spot_number=private_spot_sample.spot_number,
            venue_repository=venue_repository,
        )


def test_add_private_spot_offer_to_inexistent_social_event(
    registered_venue: Venue,
    venue_repository: VenueRepository,
    random_id: str,
):

    with pytest.raises(exceptions.SocialEventDoesNotExist):
        services.add_private_spot_offer_to_social_event(
            social_event_id=random_id,
            author_email=registered_venue.owner_email,
            spot_number=1,
            venue_repository=venue_repository,
        )


def test_add_private_spot_offer_with_not_registered_spot_number(
    registered_social_event: SocialEvent,
    venue_repository: VenueRepository,
):
    not_a_spot_number = -1
    with pytest.raises(exceptions.PrivateSpotNotFound):
        services.add_private_spot_offer_to_social_event(
            social_event_id=registered_social_event.id_str,
            author_email=registered_social_event.owner_email,
            spot_number=not_a_spot_number,
            venue_repository=venue_repository,
        )


def test_add_private_spot_offer_already_added(
    registered_social_event: SocialEvent,
    venue_repository: VenueRepository,
    private_spot_sample: PrivateSpotSample,
):
    services.add_private_spot(
        venue_id=str(registered_social_event.venue_id),
        author_email=registered_social_event.owner_email,
        venue_repository=venue_repository,
        **private_spot_sample.dict(),
    )
    services.add_private_spot_offer_to_social_event(
        social_event_id=registered_social_event.id_str,
        author_email=registered_social_event.owner_email,
        spot_number=private_spot_sample.spot_number,
        venue_repository=venue_repository,
    )

    with pytest.raises(exceptions.SpotOfferAlreadyExists):
        services.add_private_spot_offer_to_social_event(
            social_event_id=registered_social_event.id_str,
            author_email=registered_social_event.owner_email,
            spot_number=private_spot_sample.spot_number,
            venue_repository=venue_repository,
        )


def test_reserve_spot(
    registered_social_event: SocialEvent,
    sample_user_email: str,
    venue_repository: VenueRepository,
):
    available_private_spot_offer = next(
        (
            private_spot_offer
            for private_spot_offer in registered_social_event.private_spot_offers
            if private_spot_offer.available
        ),
        None,
    )
    assert available_private_spot_offer is not None
    services.reserve_spot(
        author_email=sample_user_email,
        spot_number=available_private_spot_offer.spot_number,
        social_event_id=registered_social_event.id_str,
        venue_repository=venue_repository,
    )
    social_event = services.get_social_event(
        author_email=registered_social_event.owner_email,
        social_event_id=registered_social_event.id_str,
        venue_repository=venue_repository,
    )
    private_spot_offer = next(
        (
            spot
            for spot in social_event.private_spot_offers
            if spot.spot_number == available_private_spot_offer.spot_number
        ),
        None,
    )
    assert private_spot_offer is not None
    assert not private_spot_offer.available
    assert private_spot_offer.buyer_email == sample_user_email
    assert sample_user_email in private_spot_offer.users_list


def test_reserve_spot_of_inexistent_social_event(
    sample_user_email: str,
    venue_repository: VenueRepository,
    random_id: str,
):
    spot_number = 1
    with pytest.raises(exceptions.SocialEventDoesNotExist):
        services.reserve_spot(
            author_email=sample_user_email,
            spot_number=spot_number,
            social_event_id=random_id,
            venue_repository=venue_repository,
        )


def test_reserve_not_available_spot(
    registered_social_event: SocialEvent,
    sample_user_email: str,
    venue_repository: VenueRepository,
):
    available_private_spot_offer = next(
        (
            private_spot_offer
            for private_spot_offer in registered_social_event.private_spot_offers
            if private_spot_offer.available
        ),
        None,
    )
    assert available_private_spot_offer is not None
    services.reserve_spot(
        author_email=sample_user_email,
        spot_number=available_private_spot_offer.spot_number,
        social_event_id=registered_social_event.id_str,
        venue_repository=venue_repository,
    )
    with pytest.raises(exceptions.PrivateSpotIsNotAvailable):
        services.reserve_spot(
            author_email=sample_user_email,
            spot_number=available_private_spot_offer.spot_number,
            social_event_id=registered_social_event.id_str,
            venue_repository=venue_repository,
        )


def test_reserve_inexistent_spot(
    registered_social_event: SocialEvent,
    sample_user_email: str,
    venue_repository: VenueRepository,
):
    inexistent_spot_number = -1
    with pytest.raises(exceptions.PrivateSpotOfferDoesNotExist):
        services.reserve_spot(
            author_email=sample_user_email,
            spot_number=inexistent_spot_number,
            social_event_id=registered_social_event.id_str,
            venue_repository=venue_repository,
        )


def test_join_event(
    sample_user_email: str,
    registered_social_event: SocialEvent,
    employee_list_sample: EmployeeListSample,
    venue_repository: VenueRepository,
):
    services.add_employee_list_to_social_event(
        author_email=registered_social_event.owner_email,
        employee_name=employee_list_sample.employee_name,
        code=employee_list_sample.code,
        social_event_id=registered_social_event.id_str,
        venue_repository=venue_repository,
    )
    services.join_social_event(
        author_email=sample_user_email,
        employee_code=employee_list_sample.code,
        social_event_id=registered_social_event.id_str,
        venue_repository=venue_repository,
    )
    social_event = services.get_social_event(
        author_email=registered_social_event.owner_email,
        social_event_id=registered_social_event.id_str,
        venue_repository=venue_repository,
    )
    employee_list = social_event.employee_lists[employee_list_sample.code]
    assert sample_user_email in employee_list.users


def test_join_inexistent_social_event(
    sample_user_email: str,
    employee_list_sample: EmployeeListSample,
    venue_repository: VenueRepository,
    random_id: str,
):
    with pytest.raises(exceptions.SocialEventDoesNotExist):
        services.join_social_event(
            author_email=sample_user_email,
            employee_code=employee_list_sample.code,
            social_event_id=random_id,
            venue_repository=venue_repository,
        )


def test_join_invalid_employee_list(
    sample_user_email: str,
    registered_social_event: SocialEvent,
    venue_repository: VenueRepository,
):
    invalid_employee_list_code = 'NOT_VALID'
    with pytest.raises(exceptions.EmployeeCodeDoesNotExist):
        services.join_social_event(
            author_email=sample_user_email,
            employee_code=invalid_employee_list_code,
            social_event_id=registered_social_event.id_str,
            venue_repository=venue_repository,
        )


def test_access_social_event(
    sample_user_email: str,
    registered_social_event: SocialEvent,
    venue_repository: VenueRepository,
):
    services.access_social_event(
        author_email=sample_user_email,
        social_event_id=registered_social_event.id_str,
        venue_repository=venue_repository,
    )
    social_event = services.get_social_event(
        author_email=registered_social_event.owner_email,
        social_event_id=registered_social_event.id_str,
        venue_repository=venue_repository,
    )
    assert sample_user_email in social_event.people_history
    assert sample_user_email in social_event.people_inside


def test_access_inexistent_social_event(
    sample_user_email: str,
    venue_repository: VenueRepository,
    random_id: str,
):
    with pytest.raises(exceptions.SocialEventDoesNotExist):
        services.access_social_event(
            author_email=sample_user_email,
            social_event_id=random_id,
            venue_repository=venue_repository,
        )


def test_access_twice_social_event(
    sample_user_email: str,
    registered_social_event: SocialEvent,
    venue_repository: VenueRepository,
):
    services.access_social_event(
        author_email=sample_user_email,
        social_event_id=registered_social_event.id_str,
        venue_repository=venue_repository,
    )
    services.access_social_event(
        author_email=sample_user_email,
        social_event_id=registered_social_event.id_str,
        venue_repository=venue_repository,
    )
    social_event = services.get_social_event(
        author_email=registered_social_event.owner_email,
        social_event_id=registered_social_event.id_str,
        venue_repository=venue_repository,
    )
    assert sample_user_email in social_event.people_history
    assert sample_user_email in social_event.people_inside


def test_leave_social_event(
    sample_user_email: str,
    registered_social_event: SocialEvent,
    venue_repository: VenueRepository,
):
    services.access_social_event(
        author_email=sample_user_email,
        social_event_id=registered_social_event.id_str,
        venue_repository=venue_repository,
    )
    services.leave_social_event(
        author_email=sample_user_email,
        social_event_id=registered_social_event.id_str,
        venue_repository=venue_repository,
    )
    social_event = services.get_social_event(
        author_email=registered_social_event.owner_email,
        social_event_id=registered_social_event.id_str,
        venue_repository=venue_repository,
    )
    assert sample_user_email in social_event.people_history
    assert sample_user_email not in social_event.people_inside


def test_leave_social_event_without_having_previously_accessed(
    sample_user_email: str,
    registered_social_event: SocialEvent,
    venue_repository: VenueRepository,
):
    with pytest.raises(exceptions.UserIsNotInsideTheSocialEvent):
        services.leave_social_event(
            author_email=sample_user_email,
            social_event_id=registered_social_event.id_str,
            venue_repository=venue_repository,
        )


def test_leave_inexistent_social_event(
    sample_user_email: str,
    venue_repository: VenueRepository,
    random_id: str,
):
    with pytest.raises(exceptions.SocialEventDoesNotExist):
        services.leave_social_event(
            author_email=sample_user_email,
            social_event_id=random_id,
            venue_repository=venue_repository,
        )
