import pytest

from src.profile.domain.exceptions import ProfileDoesNotExist
from src.profile.services import register_profile
from src.profile.storage.mongo_repository import ProfileMongoDB
from tests.profile.conftest import ProfileSample


def test_insert_on_db_and_has(mongo_profile_repository: ProfileMongoDB, profile_sample: ProfileSample):
    assert not mongo_profile_repository.has(email=profile_sample.email)
    register_profile(**profile_sample.dict(), profile_repository=mongo_profile_repository)
    assert mongo_profile_repository.has(email=profile_sample.email)


def test_get_returns_profile(mongo_profile_repository: ProfileMongoDB, profile_sample: ProfileSample):
    register_profile(**profile_sample.dict(), profile_repository=mongo_profile_repository)
    profile_in_db = mongo_profile_repository.get(email=profile_sample.email)
    assert profile_in_db.email == profile_sample.email


def test_get_inexistent_profile(mongo_profile_repository: ProfileMongoDB):
    with pytest.raises(ProfileDoesNotExist):
        mongo_profile_repository.get(email='inexistent_email@mail.com')
