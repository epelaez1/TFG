from types import TracebackType
from typing import Type

from pymongo import MongoClient
from pymongo.collection import Collection


class MongoDBClient:

    def __init__(self, uri: str, database: str) -> None:
        self._client = MongoClient(uri)
        self._db = self._client[database]

    def __enter__(self) -> 'MongoDBClient':
        return self

    def __exit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.close_connection()

    def get_collection(self, collection_name: str) -> Collection:
        return self._db[collection_name]

    def drop_test_database(self, db_name: str) -> None:
        if 'test' not in db_name:
            raise KeyError
        self._client.drop_database(db_name)

    def close_connection(self) -> None:
        self._client.close()
