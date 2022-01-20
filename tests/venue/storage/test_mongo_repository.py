from src.venue.domain.entities.social_event import SocialEvent
from src.venue.domain.entities.venue import Venue
from src.venue.storage.mongo_repository import VenueMongoDB
from tests.venue.conftest import VenueSample


def test_add_and_has_venue(
    mongo_venue_repository: VenueMongoDB,
    venue_sample: VenueSample,
):
    venue = Venue(**venue_sample.dict())
    assert not mongo_venue_repository.has_venue(venue_id=venue.id_str)
    mongo_venue_repository.add_venue(venue)
    assert mongo_venue_repository.has_venue(venue_id=venue.id_str)


def test_get_venue(
    mongo_venue_repository: VenueMongoDB,
    venue_sample: VenueSample,
):
    venue = Venue(**venue_sample.dict())
    mongo_venue_repository.add_venue(venue)
    saved_venue = mongo_venue_repository.get_venue(venue_id=venue.id_str)
    assert venue.dict() == saved_venue.dict()


def test_add_and_has_social_event(
    mongo_venue_repository: VenueMongoDB,
    social_event: SocialEvent,
):
    assert not mongo_venue_repository.has_social_event(social_event_id=social_event.id_str)
    mongo_venue_repository.add_social_event(social_event)
    assert mongo_venue_repository.has_social_event(social_event_id=social_event.id_str)


def test_get_social_event(
    mongo_venue_repository: VenueMongoDB,
    social_event: SocialEvent,
):
    mongo_venue_repository.add_social_event(social_event)
    saved_social_event = mongo_venue_repository.get_social_event(social_event_id=social_event.id_str)
    assert social_event == saved_social_event


def test_access_social_event(
    mongo_venue_repository: VenueMongoDB,
    social_event: SocialEvent,
    sample_user_email: str,
):
    assert sample_user_email not in social_event.people_history
    assert sample_user_email not in social_event.people_inside
    mongo_venue_repository.add_social_event(social_event)
    mongo_venue_repository.access_social_event(social_event_id=social_event.id_str, user_email=sample_user_email)
    updated_social_event = mongo_venue_repository.get_social_event(social_event_id=social_event.id_str)
    assert sample_user_email in updated_social_event.people_history
    assert sample_user_email in updated_social_event.people_inside


def test_leave_social_event(
    mongo_venue_repository: VenueMongoDB,
    social_event: SocialEvent,
    sample_user_email: str,
):
    mongo_venue_repository.add_social_event(social_event)
    mongo_venue_repository.access_social_event(social_event_id=social_event.id_str, user_email=sample_user_email)
    mongo_venue_repository.leave_social_event(social_event_id=social_event.id_str, user_email=sample_user_email)
    updated_social_event = mongo_venue_repository.get_social_event(social_event_id=social_event.id_str)
    assert sample_user_email in updated_social_event.people_history
    assert sample_user_email not in updated_social_event.people_inside


def test_join_social_event(
    mongo_venue_repository: VenueMongoDB,
    social_event: SocialEvent,
    sample_user_email: str,
):
    employee_list_code = 'SOME_CODE'
    employee_name = 'Some Name'
    social_event.add_employee_list(code=employee_list_code, employee_name=employee_name)
    mongo_venue_repository.add_social_event(social_event)
    mongo_venue_repository.join_social_event(
        social_event_id=social_event.id_str,
        employee_code=employee_list_code,
        user_email=sample_user_email,
    )
    updated_social_event = mongo_venue_repository.get_social_event(social_event_id=social_event.id_str)
    assert sample_user_email in updated_social_event.employee_lists[employee_list_code].users
