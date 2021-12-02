import json
from datetime import datetime
from datetime import timedelta
from typing import Any

import pytest
from jose import jwt

from src.authentication import services
from src.authentication.domain import exceptions
from src.authentication.domain.entities.session import SessionToken
from src.authentication.domain.repository import CredentialsRepository
from tests.authentication.conftest import CredentialsSample


def test_register_new_user(
    credentials_repository: CredentialsRepository,
    credentials_sample: CredentialsSample,
    secret_key: str,
):
    register_response = services.register_user(
        **credentials_sample.dict(), credentials_repository=credentials_repository, secret_key=secret_key,
    )
    assert credentials_repository.has(credentials_sample.email)
    saved_credentials = credentials_repository.get(email=credentials_sample.email)
    assert saved_credentials.hashed_password != credentials_sample.password
    assert not saved_credentials.has_profile
    assert 'access_token' in register_response.json()


def test_login_ang_get_session_token_data(
    credentials_repository: CredentialsRepository,
    credentials_sample: CredentialsSample,
    secret_key: str,
):
    services.register_user(
        **credentials_sample.dict(), credentials_repository=credentials_repository, secret_key=secret_key,
    )
    token: SessionToken = services.login(
        email=credentials_sample.email,
        password=credentials_sample.password,
        credentials_repository=credentials_repository,
        secret_key=secret_key,
    )
    assert isinstance(token, SessionToken)
    user_token_data = services.get_session_token_data(token=token.access_token, secret_key=secret_key)
    assert user_token_data.email == credentials_sample.email


def test_login_with_incorrect_password(
    credentials_repository: CredentialsRepository,
    credentials_sample: CredentialsSample,
    secret_key: str,
):
    services.register_user(
        **credentials_sample.dict(), credentials_repository=credentials_repository, secret_key=secret_key,
    )
    with pytest.raises(exceptions.IncorrectPassword):
        services.login(  # noqa: S106
            email=credentials_sample.email,
            password='wrong_password',
            credentials_repository=credentials_repository,
            secret_key=secret_key,
        )


def test_login_with_inexistent_user(
    credentials_repository: CredentialsRepository,
    credentials_sample: CredentialsSample,
    secret_key: str,
):
    with pytest.raises(exceptions.IncorrectUsername):
        services.login(
            email='inexistent_user@mail.com',
            password=credentials_sample.password,
            credentials_repository=credentials_repository,
            secret_key=secret_key,
        )


def test_get_session_token_data(valid_session_token: str, secret_key: str, credentials_sample: CredentialsSample):
    user_token_data = services.get_session_token_data(token=valid_session_token, secret_key=secret_key)
    assert user_token_data.email == credentials_sample.email


def test_get_email_from_expired_token(secret_key: str, token_info: dict[str, str | datetime]):
    expired_token_info: dict[str, Any] = {**token_info, 'exp': datetime.utcnow() - timedelta(minutes=1)}
    expired_token = jwt.encode(expired_token_info, secret_key)
    with pytest.raises(exceptions.Unauthorized):
        services.get_session_token_data(token=expired_token, secret_key=secret_key)


def test_get_session_token_data_without_sub(secret_key: str, token_info: dict[str, str | datetime]):
    token_info_without_sub = token_info.copy()
    token_info_without_sub.pop('sub')
    no_sub_token = jwt.encode(token_info_without_sub, secret_key)
    with pytest.raises(exceptions.Unauthorized):
        services.get_session_token_data(token=no_sub_token, secret_key=secret_key)


@pytest.mark.parametrize(
    'sub',
    [
        str({}),
        '',
        str([]),
        json.dumps({'email': ''}),
    ],
)
def test_get_session_token_data_with_bad_sub(secret_key: str, token_info: dict[str, str | datetime], sub: Any):
    token_info_with_empty_mail: dict[str, Any] = {**token_info, 'sub': sub}  # TODO
    empty_mail_token = jwt.encode(token_info_with_empty_mail, secret_key)
    with pytest.raises(exceptions.Unauthorized):
        services.get_session_token_data(token=empty_mail_token, secret_key=secret_key)


def test_get_email_from_bad_signed_token(secret_key: str, token_info: dict[str, str | datetime]):
    other_secret_key = '91eaddafe18f273360800647aa08965f9cccbc1248d5748975a743d0f4b03ee6'  # noqa: S105
    bad_signature_token = jwt.encode(token_info, other_secret_key)
    with pytest.raises(exceptions.Unauthorized):
        services.get_session_token_data(token=bad_signature_token, secret_key=secret_key)
