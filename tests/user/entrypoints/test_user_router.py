from fastapi import FastAPI
from fastapi import status
from fastapi.testclient import TestClient

from src.error_models import APIError
from src.user.entrypoints import exception_handlers
from tests.user.conftest import UserSample

REGISTER_USER = 'user:register'
LOGIN = 'user:login'
MY_USER = 'user:my-user'


def test_register_new_user(app: FastAPI, app_client: TestClient, user_sample: UserSample):
    response = app_client.post(app.url_path_for(REGISTER_USER), json=user_sample.dict())
    expected_response: dict[str, str | bool] = {**user_sample.dict(), 'verified': False}
    expected_response.pop('password')
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == expected_response


def test_register_with_user_already_registered(app: FastAPI, app_client: TestClient, user_sample: UserSample):
    app_client.post(app.url_path_for(REGISTER_USER), json=user_sample.dict())
    response = app_client.post(app.url_path_for(REGISTER_USER), json=user_sample.dict())
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    error_details = APIError(**response.json())
    assert error_details.error_code == exception_handlers.USER_ALREADY_REGISTERED_ERROR_CODE


def test_bad_email_returns_validation_error(app: FastAPI, app_client: TestClient, user_sample: UserSample):
    user_sample.email = 'not_an_email'
    response = app_client.post(app.url_path_for(REGISTER_USER), json=user_sample.dict())
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()['detail'][0]['type'] == 'value_error.email'


def test_login_and_get_user(app: FastAPI, app_client: TestClient, user_sample: UserSample):  # noqa: WPS 210
    app_client.post(app.url_path_for(REGISTER_USER), json=user_sample.dict())
    form_data = {
        'username': user_sample.email,
        'password': user_sample.password,
    }
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
    }
    login_response = app_client.post(app.url_path_for(LOGIN), data=form_data, headers=headers)
    assert login_response.status_code == status.HTTP_200_OK

    token = login_response.json()['access_token']
    app_client.headers['authorization'] = f'Bearer {token}'
    get_user_response = app_client.get(app.url_path_for(MY_USER))
    assert get_user_response.status_code == status.HTTP_200_OK

    expected_response = {**user_sample.dict(), 'verified': False}
    expected_response.pop('password')
    assert expected_response == get_user_response.json()
