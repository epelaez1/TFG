from datetime import datetime
from datetime import timedelta

import pytest
from pydantic import BaseModel

from src.user.domain.user import register_new_user
from src.user.domain.user import User
from src.user.domain.user_repository import BasicUserRepository
from src.user.domain.user_repository import UserRepository
from src.user.storage.mongo_user_repository import UserMongoDB


class UserSample(BaseModel):
    email: str = 'new_user@mail.es'
    name: str = 'bob'
    phone: str = '+34654321321'
    password: str = 'test_password'


@pytest.fixture
def user_repository() -> UserRepository:
    return BasicUserRepository()


@pytest.fixture
def user_sample() -> UserSample:
    return UserSample()


@pytest.fixture
def mongo_user_repository(mongo_client):
    return UserMongoDB(client=mongo_client)


@pytest.fixture
def valid_user_token(user_sample: UserSample, user_repository: UserRepository, secret_key: str):  # noqa: WPS442
    user: User = register_new_user(**user_sample.dict(), user_repository=user_repository)
    return user.get_session_token(secret_key=secret_key).access_token


@pytest.fixture
def token_info():
    return {
        'sub': 'new_user@mail.es',
        'exp': datetime.utcnow() + timedelta(minutes=1),
    }
