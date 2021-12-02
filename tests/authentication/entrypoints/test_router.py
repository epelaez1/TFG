from fastapi import FastAPI
from fastapi import status
from fastapi.testclient import TestClient

from src.authentication.entrypoints import exception_handlers
from src.error_models import APIError
from tests.authentication.conftest import CredentialsSample

REGISTER_USER = 'auth:register'
LOGIN = 'auth:login'


def test_register_new_user(app: FastAPI, app_client: TestClient, credentials_sample: CredentialsSample):
    response = app_client.post(app.url_path_for(REGISTER_USER), json=credentials_sample.dict())
    assert response.status_code == status.HTTP_201_CREATED
    assert 'access_token' in response.json()
    assert 'token_type' in response.json()


def test_register_with_email_already_registered(
    app: FastAPI,
    app_client: TestClient,
    credentials_sample: CredentialsSample,
):
    first_response = app_client.post(app.url_path_for(REGISTER_USER), json=credentials_sample.dict())
    assert first_response.status_code == status.HTTP_201_CREATED
    response = app_client.post(app.url_path_for(REGISTER_USER), json=credentials_sample.dict())
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    error_details = APIError(**response.json())
    assert error_details.error_code == exception_handlers.USER_ALREADY_REGISTERED


def test_bad_email_returns_validation_error(
    app: FastAPI,
    app_client: TestClient,
    credentials_sample: CredentialsSample,
):
    credentials_sample.email = 'not_an_email'
    response = app_client.post(app.url_path_for(REGISTER_USER), json=credentials_sample.dict())
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()['detail'][0]['type'] == 'value_error.email'


def test_login(app: FastAPI, app_client: TestClient, credentials_sample: CredentialsSample):  # noqa: WPS 210
    app_client.post(app.url_path_for(REGISTER_USER), json=credentials_sample.dict())
    form_data = {
        'username': credentials_sample.email,
        'password': credentials_sample.password,
    }
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
    }
    login_response = app_client.post(app.url_path_for(LOGIN), data=form_data, headers=headers)
    assert login_response.status_code == status.HTTP_200_OK
