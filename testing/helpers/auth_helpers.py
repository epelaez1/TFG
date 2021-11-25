from fastapi import FastAPI
from fastapi.testclient import TestClient

LOGIN = 'auth:login'


def login(app: FastAPI, app_client: TestClient, username: str, password: str):
    form_data = {
        'username': username,
        'password': password,
    }
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
    }
    login_response = app_client.post(app.url_path_for(LOGIN), data=form_data, headers=headers)
    token = login_response.json()['access_token']
    app_client.headers['authorization'] = f'Bearer {token}'
