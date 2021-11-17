from src.config import environment
from src.config import mongo_settings
from src.mongo_client import MongoDBClient
from src.user.domain.user_repository import BasicUserRepository
from src.user.storage.mongo_user_repository import UserMongoDB


mongo_client = MongoDBClient(uri=mongo_settings.uri, database=mongo_settings.database)
user_repository = BasicUserRepository() if environment.is_test else UserMongoDB(client=mongo_client)
