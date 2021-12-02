from fastapi import FastAPI
from fastapi import status
from fastapi.testclient import TestClient


SERVICE_INFO = 'service-info'


def test_info_returns_ok(app: FastAPI, app_client: TestClient) -> None:
    response = app_client.get(app.url_path_for(SERVICE_INFO))
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'status': 'ok'}
