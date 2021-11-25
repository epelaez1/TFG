import pytest

from src.profile import profile_services
from src.profile.domain import exceptions
from src.profile.domain.profile_repository import ProfileRepository
from tests.profile.conftest import ProfileSample


def test_new_profile_register(profile_repository: ProfileRepository, profile_sample: ProfileSample):
    new_profile = profile_services.register_profile(**profile_sample.dict(), profile_repository=profile_repository)
    assert profile_repository.has(new_profile.email)
    assert new_profile.email == profile_sample.email
    assert new_profile.phone == profile_sample.phone
    assert new_profile.name == profile_sample.name


def test_register_existing_profile(profile_repository: ProfileRepository, profile_sample: ProfileSample):
    profile_services.register_profile(**profile_sample.dict(), profile_repository=profile_repository)
    with pytest.raises(exceptions.ProfileAlreadyInitialized):
        profile_services.register_profile(**profile_sample.dict(), profile_repository=profile_repository)


def test_get_profile(profile_repository: ProfileRepository, profile_sample: ProfileSample):
    registered_profile = profile_services.register_profile(
        **profile_sample.dict(),
        profile_repository=profile_repository,
    )
    profile_from_db = profile_services.get_profile(email=profile_sample.email, profile_repository=profile_repository)
    assert profile_from_db == registered_profile


def test_get_inexistent_profile(profile_repository: ProfileRepository):
    with pytest.raises(exceptions.ProfileDoesNotExist):
        profile_services.get_profile(email='inexistent_profile@mail.es', profile_repository=profile_repository)
