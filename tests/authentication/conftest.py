import json
from datetime import datetime
from datetime import timedelta

import pytest
from pydantic import BaseModel

from src.authentication.auth_services import register_user
from src.authentication.domain.credentials import Credentials
from src.authentication.domain.credentials import TokenData
from src.authentication.domain.credentials_repository import BasicCredentialsRepository
from src.authentication.domain.credentials_repository import CredentialsRepository
from src.authentication.domain.session import SessionToken
from src.authentication.storage.mongo_cred_repository import CredentialsMongoDB


class CredentialsSample(BaseModel):
    email: str = 'new_mail@mail.es'
    password: str = 'test_password'


@pytest.fixture
def credentials_repository() -> CredentialsRepository:
    return BasicCredentialsRepository()


@pytest.fixture
def credentials_sample() -> CredentialsSample:
    return CredentialsSample()


@pytest.fixture
def mongo_credentials_repository(mongo_client):
    return CredentialsMongoDB(client=mongo_client)


@pytest.fixture
def valid_session_token(
    credentials_sample: CredentialsSample,  # noqa: WPS442
    credentials_repository: CredentialsRepository,  # noqa: WPS442
    secret_key: str,
):
    session_token: SessionToken = register_user(
        **credentials_sample.dict(),
        credentials_repository=credentials_repository,
        secret_key=secret_key,
    )
    return session_token.access_token


@pytest.fixture
def token_info(
    credentials_sample: Credentials,  # noqa: WPS442
):
    token_data = TokenData(**credentials_sample.dict())
    return {
        'sub': json.dumps(token_data.dict()),
        'exp': datetime.utcnow() + timedelta(minutes=1),
    }
