import pytest
from bson import ObjectId

from src.social_event import social_event_services
from src.social_event.domain import exceptions
from src.social_event.domain.social_event_repository import SocialEventRepository
from tests.social_event.conftest import SocialEventSample


def test_create_social_event(
    social_event_sample: SocialEventSample,
    social_event_repository: SocialEventRepository,
):
    social_event_id = social_event_services.create(
        **social_event_sample.dict(),
        social_event_repository=social_event_repository,
    )
    assert social_event_repository.has(social_event_id=social_event_id)


def test_get_social_event(
    social_event_sample: SocialEventSample,
    social_event_repository: SocialEventRepository,
):
    social_event_id = social_event_services.create(
        **social_event_sample.dict(),
        social_event_repository=social_event_repository,
    )
    social_event = social_event_services.get(
        social_event_id=social_event_id,
        social_event_repository=social_event_repository,
    )

    assert str(social_event.id) == social_event_id
    assert social_event_sample.name == social_event.name
    assert social_event_sample.description == social_event.description
    assert social_event_sample.start_date == social_event.start_date
    assert social_event_sample.end_date == social_event.end_date


def test_get_inexistent_social_event(
    social_event_repository: SocialEventRepository,
):
    with pytest.raises(exceptions.SocialEventDoesNotExist):
        social_event_repository.get(str(ObjectId()))
