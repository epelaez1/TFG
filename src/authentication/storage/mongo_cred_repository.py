from typing import Any

from pymongo.collection import Collection

from src.authentication.domain import exceptions
from src.authentication.domain.credentials import Credentials
from src.authentication.domain.credentials_repository import CredentialsRepository
from src.mongo_client import MongoDBClient

AUTH_COLLECTION = 'authentication'


class CredentialsMongoDB(CredentialsRepository):

    def __init__(self, client: MongoDBClient) -> None:
        self._client = client
        self.auth_collection: Collection = self._client.get_collection(AUTH_COLLECTION)

    def has(self, email: str) -> bool:
        return int(self.auth_collection.count_documents({'email': email})) == 1

    def add(self, credentials: Credentials) -> None:
        self.auth_collection.insert_one(credentials.dict())

    def get(self, email: str) -> Credentials:
        credentials_in_db: dict[str, Any] = self.auth_collection.find_one({'email': email})
        if credentials_in_db is None:
            raise exceptions.UserDoesNotExist()
        return Credentials(**credentials_in_db)

    def update(self, email: str, new_credentials: Credentials) -> None:
        self.auth_collection.update_one({'email': email}, {'$set': new_credentials.dict()})
