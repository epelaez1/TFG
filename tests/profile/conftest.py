import pytest
from fastapi.applications import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

from src.profile.domain.profile_repository import BasicProfileRepository
from src.profile.domain.profile_repository import ProfileRepository
from src.profile.storage.mongo_profile_repository import ProfileMongoDB

REGISTER_USER = 'auth:register'
LOGIN = 'auth:login'
REGISTER_PROFILE = 'profile:register'


class ProfileFormSample(BaseModel):
    name: str = 'bob'
    phone: str = '+34654321321'


class ProfileSample(ProfileFormSample):
    email: str = 'new_mail@mail.es'


class CredentialsSample(BaseModel):
    email: str = 'new_mail@mail.es'
    password: str = 'test_password'


@pytest.fixture
def profile_repository() -> ProfileRepository:
    return BasicProfileRepository()


@pytest.fixture
def profile_sample() -> ProfileSample:
    return ProfileSample()


@pytest.fixture
def mongo_profile_repository(mongo_client):
    return ProfileMongoDB(client=mongo_client)


@pytest.fixture
def user_without_profile_credentials() -> CredentialsSample:
    return CredentialsSample(email='no_profile@mail.es', password='test_password')  # noqa: S106


@pytest.fixture
def verified_user_credentials() -> CredentialsSample:
    return CredentialsSample(email='verified_user@mail.es', password='verified_user_password')  # noqa: S106


@pytest.fixture
def verified_user_profile() -> ProfileFormSample:
    return ProfileFormSample(name='verified_user', phone='654654654')


@pytest.fixture
def seeded_client(
    app_client: TestClient,
    app: FastAPI,
    user_without_profile_credentials: CredentialsSample,  # noqa: WPS442
    verified_user_credentials: CredentialsSample,  # noqa: WPS442
    verified_user_profile: ProfileFormSample,  # noqa: WPS442
) -> TestClient:
    app_client.post(app.url_path_for(REGISTER_USER), json=user_without_profile_credentials.dict())
    register_response = app_client.post(app.url_path_for(REGISTER_USER), json=verified_user_credentials.dict())
    token = register_response.json()['access_token']
    headers = {
        'authorization': f'Bearer {token}',
    }
    app_client.post(app.url_path_for(REGISTER_PROFILE), headers=headers, json=verified_user_profile.dict())
    return app_client
