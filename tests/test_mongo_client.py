import pytest

from src.mongo_client import MongoDBClient

NON_TEST_DB = 'non_dropable_db'


def test_mongo_client_cant_drop_a_non_test_db(mongo_client: MongoDBClient):
    with pytest.raises(KeyError):
        mongo_client.drop_test_database(NON_TEST_DB)
