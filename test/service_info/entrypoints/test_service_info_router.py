from fastapi import status
from fastapi.testclient import TestClient


def test_info_returns_ok(app_client: TestClient) -> None:
    response = app_client.get('/service_info/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'status': 'ok'}
