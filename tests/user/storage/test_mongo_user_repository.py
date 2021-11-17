import pytest

from src.user.storage.mongo_user_repository import UserMongoDB
from src.user.user_services import register_user
from tests.user.conftest import UserSample


def test_insert_on_db_and_has(mongo_user_repository: UserMongoDB, user_sample: UserSample):
    assert not mongo_user_repository.has(email=user_sample.email)
    register_user(**user_sample.dict(), user_repository=mongo_user_repository)
    assert mongo_user_repository.has(email=user_sample.email)


def test_get_returns_user(mongo_user_repository: UserMongoDB, user_sample: UserSample):
    register_user(**user_sample.dict(), user_repository=mongo_user_repository)
    user_in_db = mongo_user_repository.get(email=user_sample.email)
    assert user_in_db.email == user_sample.email


def test_get_inexistent_user_raises_value_error(mongo_user_repository: UserMongoDB):
    with pytest.raises(ValueError):
        mongo_user_repository.get(email='inexistent_email@mail.com')
