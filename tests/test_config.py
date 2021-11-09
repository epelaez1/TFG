import os

from dotenv import load_dotenv

from src.config import mongo_settings

LOCAL_MONGODB_URI = 'mongodb://127.0.0.1:27017'


def test_mongo_db_config_return_default():
    load_dotenv()
    assert mongo_settings.uri == (os.getenv('MONGO_DB_URI') or LOCAL_MONGODB_URI)
