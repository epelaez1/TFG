from fastapi import FastAPI
from fastapi import status
from fastapi.testclient import TestClient

from src.authentication.entrypoints import exception_handlers as auth_exception_handlers
from src.error_models import APIError
from src.profile.entrypoints import exception_handlers as profile_exception_handlers
from testing.helpers.auth_helpers import login
from tests.profile.conftest import CredentialsSample
from tests.profile.conftest import ProfileSample

LOGIN = 'auth:login'
REGISTER_PROFILE = 'profile:register'
MY_USER = 'profile:my-profile'


def test_register_new_profile(
    app: FastAPI,
    seeded_client: TestClient,
    user_without_profile_credentials: CredentialsSample,
    profile_sample: ProfileSample,
):
    login(
        app=app,
        app_client=seeded_client,
        username=user_without_profile_credentials.email,
        password=user_without_profile_credentials.password,
    )
    response = seeded_client.post(app.url_path_for(REGISTER_PROFILE), json=profile_sample.dict())
    assert response.status_code == status.HTTP_201_CREATED
    assert 'access_token' in response.json()
    assert 'token_type' in response.json()


def test_register_with_profile_already_registered(
    app: FastAPI,
    seeded_client: TestClient,
    user_without_profile_credentials: CredentialsSample,
    profile_sample: ProfileSample,
):
    login(
        app=app,
        app_client=seeded_client,
        username=user_without_profile_credentials.email,
        password=user_without_profile_credentials.password,
    )
    seeded_client.post(app.url_path_for(REGISTER_PROFILE), json=profile_sample.dict())
    response = seeded_client.post(app.url_path_for(REGISTER_PROFILE), json=profile_sample.dict())
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    error_details = APIError(**response.json())
    assert error_details.error_code == profile_exception_handlers.PROFILE_ALREADY_INITIALIZED


def test_get_profile(
    app: FastAPI,
    seeded_client: TestClient,
    verified_user_credentials: CredentialsSample,
    verified_user_profile: ProfileSample,
):
    login(
        app_client=seeded_client,
        app=app,
        username=verified_user_credentials.email,
        password=verified_user_credentials.password,
    )
    get_profile_response = seeded_client.get(app.url_path_for(MY_USER))
    expected_response = {**verified_user_profile.dict(), 'email': verified_user_credentials.email}
    assert get_profile_response.status_code == status.HTTP_200_OK
    assert expected_response == get_profile_response.json()


def test_get_inexistent_profile(
    app: FastAPI,
    seeded_client: TestClient,
    user_without_profile_credentials: CredentialsSample,
):
    login(
        app=app,
        app_client=seeded_client,
        username=user_without_profile_credentials.email,
        password=user_without_profile_credentials.password,
    )
    get_profile_response = seeded_client.get(app.url_path_for(MY_USER))
    assert get_profile_response.status_code == status.HTTP_401_UNAUTHORIZED
    error_details = APIError(**get_profile_response.json())
    assert error_details.error_code == auth_exception_handlers.USER_WITHOT_PROFILE
