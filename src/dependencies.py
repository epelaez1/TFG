from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from src.authentication import services
from src.authentication.domain.entities.credentials import TokenData
from src.authentication.domain.repository import BasicCredentialsRepository
from src.authentication.storage.mongo_repository import CredentialsMongoDB
from src.config import environment
from src.config import mongo_settings
from src.mongo_client import MongoDBClient
from src.profile.domain.repository import BasicProfileRepository
from src.profile.storage.mongo_repository import ProfileMongoDB
from src.venue.domain.repository import BasicVenueRepository
from src.venue.storage. mongo_repository import VenueMongoDB

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')


async def profile_creation_email(token: str = Depends(oauth2_scheme)) -> str:
    token_data: TokenData = services.authorize_profile_creation(token=token, secret_key=environment.secret_key)
    return token_data.email


async def authorized_user_email(token: str = Depends(oauth2_scheme)) -> str:
    token_data = services.authorize(token=token, secret_key=environment.secret_key)
    return token_data.email


class Repositories:
    def __init__(self) -> None:
        self.mongo_client = MongoDBClient(uri=mongo_settings.uri, database=mongo_settings.database)
        self.reload_repositories()

    def reload_repositories(self) -> None:
        self.profile_repository = (
            BasicProfileRepository()
            if environment.is_test
            else ProfileMongoDB(client=self.mongo_client)
        )
        self.credentials_repository = (
            BasicCredentialsRepository()
            if environment.is_test
            else CredentialsMongoDB(client=self.mongo_client)
        )
        self.venue_repository = (
            BasicVenueRepository()
            if environment.is_test
            else VenueMongoDB(client=self.mongo_client)
        )


repositories = Repositories()
