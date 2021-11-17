from typing import Any

from pymongo.collection import Collection

from src.mongo_client import MongoDBClient
from src.user.domain.user import User
from src.user.domain.user_repository import UserRepository

USER_COLLECTION = 'users'


class UserMongoDB(UserRepository):

    def __init__(self, client: MongoDBClient) -> None:
        self._client = client
        self.user_collection: Collection = self._client.get_collection(USER_COLLECTION)

    def has(self, email: str) -> bool:
        return int(self.user_collection.count_documents({'email': email})) == 1

    def add(self, user: User) -> None:
        self.user_collection.insert_one(user.dict())

    def get(self, email: str) -> User:
        user_in_db: dict[str, Any] = self.user_collection.find_one({'email': email})
        if user_in_db is None:
            raise ValueError
        return User(**user_in_db)
