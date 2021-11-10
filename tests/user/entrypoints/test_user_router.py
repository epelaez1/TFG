from fastapi import status
from fastapi.testclient import TestClient

REGISTER_USER_ENDPOINT = '/user/'


def test_register_new_user(app_client: TestClient, user_sample: dict[str, str]):
    response = app_client.post(REGISTER_USER_ENDPOINT, json=user_sample)
    expected_response: dict[str, str | bool] = {**user_sample, 'verified': False}
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == expected_response


def test_register_with_user_already_registered(app_client: TestClient, user_sample: dict[str, str]):
    app_client.post(REGISTER_USER_ENDPOINT, json=user_sample)
    response = app_client.post(REGISTER_USER_ENDPOINT, json=user_sample)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_bad_email_returns_validation_error(app_client: TestClient, user_sample: dict[str, str]):
    user_sample['email'] = 'not_an_email'
    response = app_client.post(REGISTER_USER_ENDPOINT, json=user_sample)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()['detail'][0]['type'] == 'value_error.email'
