import pytest

from src.authentication.domain import exceptions
from src.authentication.services import register_user
from src.authentication.services import update_profile
from src.authentication.storage.mongo_repository import CredentialsMongoDB
from tests.authentication.conftest import CredentialsSample


def test_insert_cred_on_db_and_has(
    mongo_credentials_repository: CredentialsMongoDB,
    credentials_sample: CredentialsSample,
    secret_key: str,
):
    assert not mongo_credentials_repository.has(email=credentials_sample.email)
    register_user(
        **credentials_sample.dict(), credentials_repository=mongo_credentials_repository, secret_key=secret_key,
    )
    assert mongo_credentials_repository.has(email=credentials_sample.email)


def test_get_returns_credentials(
    mongo_credentials_repository: CredentialsMongoDB,
    credentials_sample: CredentialsSample,
    secret_key: str,
):
    register_user(
        **credentials_sample.dict(), credentials_repository=mongo_credentials_repository, secret_key=secret_key,
    )
    credentials_in_db = mongo_credentials_repository.get(email=credentials_sample.email)
    assert credentials_in_db.email == credentials_sample.email


def test_get_inexistent_credentials(mongo_credentials_repository: CredentialsMongoDB):
    with pytest.raises(exceptions.UserDoesNotExist):
        mongo_credentials_repository.get(email='inexistent_email@mail.com')


def test_update_credentials(
    mongo_credentials_repository: CredentialsMongoDB,
    credentials_sample: CredentialsSample,
    secret_key: str,
):
    register_user(
        **credentials_sample.dict(), credentials_repository=mongo_credentials_repository, secret_key=secret_key,
    )
    assert mongo_credentials_repository.has(email=credentials_sample.email)
    update_profile(
        email=credentials_sample.email,
        credentials_repository=mongo_credentials_repository,
        secret_key=secret_key,
    )
    credentials_in_db = mongo_credentials_repository.get(email=credentials_sample.email)
    assert credentials_in_db.has_profile
