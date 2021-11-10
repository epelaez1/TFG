from src.user.storage.mongo_user_repository import UserMongoDB
from src.user.user_services import register_user


def test_insert_on_db_and_has(mongo_user_repository: UserMongoDB, user_sample: dict[str, str]):
    assert not mongo_user_repository.has(email=user_sample['email'])
    register_user(**user_sample, user_repository=mongo_user_repository)
    assert mongo_user_repository.has(email=user_sample['email'])
