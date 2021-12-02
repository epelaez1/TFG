from typing import Any

from pymongo.collection import Collection

from src.mongo_client import MongoDBClient
from src.profile.domain.entities.profile import Profile
from src.profile.domain.exceptions import ProfileDoesNotExist
from src.profile.domain.repository import ProfileRepository

USER_COLLECTION = 'profiles'


class ProfileMongoDB(ProfileRepository):

    def __init__(self, client: MongoDBClient) -> None:
        self._client = client
        self.profile_collection: Collection = self._client.get_collection(USER_COLLECTION)

    def has(self, email: str) -> bool:
        return int(self.profile_collection.count_documents({'email': email})) == 1

    def add(self, profile: Profile) -> None:
        self.profile_collection.insert_one(profile.dict())

    def get(self, email: str) -> Profile:
        profile_in_db: dict[str, Any] = self.profile_collection.find_one({'email': email})
        if profile_in_db is None:
            raise ProfileDoesNotExist()
        return Profile(**profile_in_db)
