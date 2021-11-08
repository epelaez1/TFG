from fastapi import status
from fastapi.testclient import TestClient

endpoints = {
    'register_user': '/user/'
}


def test_create_user_endpoint_returns_new_user(app_client: TestClient, user_sample: dict[str, str]):
    response = app_client.post(endpoints['register_user'], json=user_sample)
    expected_response: dict[str, str | bool] = {**user_sample, 'verified': False}
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == expected_response


def test_user_endpoint_returns_400_if_user_exists(app_client: TestClient, user_sample: dict[str, str]):
    app_client.post(endpoints['register_user'], json=user_sample)
    response = app_client.post(endpoints['register_user'], json=user_sample)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_bad_email_returns_validation_error(app_client: TestClient, user_sample: dict[str, str]):
    user_sample['email'] = 'not_an_email'
    response = app_client.post(endpoints['register_user'], json=user_sample)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()['detail'][0]['type'] == 'value_error.email'
