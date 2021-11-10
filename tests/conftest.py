import pytest
from fastapi.testclient import TestClient

from main import app
from src.user.domain.user_repository import BasicUserRepository
from src.user.domain.user_repository import UserRepository


@pytest.fixture
def app_client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def user_repository() -> UserRepository:
    return BasicUserRepository()


@pytest.fixture
def user_sample() -> dict[str, str]:
    return {
        'email': 'new_user@mail.es',
        'name': 'bob',
        'phone': '6543213210',
    }
