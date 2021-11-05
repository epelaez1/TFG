import pytest
from fastapi.testclient import TestClient

from main import app
from src.user.domain.user_repository import UserRepository
from src.user.domain.user_repository import BasicUserRepository


@pytest.fixture
def app_client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def user_repository() -> UserRepository:
    return BasicUserRepository()
