import pytest
from fastapi.testclient import TestClient

from main import app
from src.config import mongo_settings
from src.mongo_client import MongoDBClient
from src.user.domain.user_repository import BasicUserRepository
from src.user.domain.user_repository import UserRepository
from src.user.storage.mongo_user_repository import UserMongoDB

TEST_DB_NAME = 'tfg_testing_db'


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


@pytest.fixture
def mongo_user_repository():
    with MongoDBClient(uri=mongo_settings.uri, database=TEST_DB_NAME) as db_client:
        yield UserMongoDB(client=db_client)
        db_client.drop_test_database(TEST_DB_NAME)


@pytest.fixture
def mongo_client():
    with MongoDBClient(uri=mongo_settings.uri, database=TEST_DB_NAME) as db_client:
        yield db_client
        db_client.drop_test_database(TEST_DB_NAME)
