from pydantic import BaseSettings


class Settings(BaseSettings):
    class Config:
        env_file = '.env'


class MongoDBSettings(Settings):
    uri: str = 'mongodb://127.0.0.1:27017'
    database: str = 'tfg_local'

    class Config(Settings.Config):
        env_prefix = 'MONGO_DB_'


class Environment(Settings):
    is_production: bool = False

    class Config(Settings.Config):
        env_prefix = 'ENV_'


mongo_settings = MongoDBSettings()
environment = Environment()
