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
    is_test: bool = True
    secret_key: str = '84fe28918b95361efad1b4c394a1fa1db2be0ba2ba3eb1b93eaa816ec094097e'

    class Config(Settings.Config):
        env_prefix = 'ENV_'


mongo_settings = MongoDBSettings()
environment = Environment()
