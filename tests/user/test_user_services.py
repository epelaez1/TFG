from datetime import datetime
from datetime import timedelta
from typing import Any

import pytest
from jose import jwt

from src.user import user_services
from src.user.domain import exceptions
from src.user.domain.session import SessionToken
from src.user.domain.user_repository import UserRepository
from tests.user.conftest import UserSample


def test_new_user_register(user_repository: UserRepository, user_sample: UserSample):
    new_user = user_services.register_user(**user_sample.dict(), user_repository=user_repository)
    assert user_repository.has(new_user.email)
    assert new_user.hashed_password != user_sample.password
    assert not new_user.verified


def test_register_existing_user_raise_exception(user_repository: UserRepository, user_sample: UserSample):
    user_services.register_user(**user_sample.dict(), user_repository=user_repository)
    with pytest.raises(exceptions.UserAlreadyRegistered):
        user_services.register_user(**user_sample.dict(), user_repository=user_repository)


def test_login_ang_get_email_from_token(user_repository: UserRepository, user_sample: UserSample, secret_key: str):
    user_services.register_user(**user_sample.dict(), user_repository=user_repository)
    token: SessionToken = user_services.login(
        email=user_sample.email,
        password=user_sample.password,
        user_repository=user_repository,
        secret_key=secret_key,
    )
    assert isinstance(token, SessionToken)
    user_email = user_services.get_email_from_token(token=token.access_token, secret_key=secret_key)
    assert user_email == user_sample.email


def test_login_with_incorrect_password(user_repository: UserRepository, user_sample: UserSample, secret_key: str):
    user_services.register_user(**user_sample.dict(), user_repository=user_repository)
    with pytest.raises(exceptions.IncorrectPassword):
        user_services.login(  # noqa: S106
            email=user_sample.email,
            password='wrong_password',
            user_repository=user_repository,
            secret_key=secret_key,
        )


def test_login_with_inexistent_user(user_repository: UserRepository, user_sample: UserSample, secret_key: str):
    with pytest.raises(exceptions.IncorrectUsername):
        user_services.login(
            email='inexistent_user@mail.com',
            password=user_sample.password,
            user_repository=user_repository,
            secret_key=secret_key,
        )


def test_get_user(user_repository: UserRepository, user_sample: UserSample):
    registered_user = user_services.register_user(**user_sample.dict(), user_repository=user_repository)
    user_from_db = user_services.get_user(email=user_sample.email, user_repository=user_repository)
    assert user_from_db == registered_user


def test_get_inexistent_user(user_repository: UserRepository):
    with pytest.raises(exceptions.UserDoesNotExists):
        user_services.get_user(email='inexistent_user@mail.es', user_repository=user_repository)


def test_get_email_from_token(valid_user_token: str, secret_key: str, user_sample: UserSample):
    email = user_services.get_email_from_token(token=valid_user_token, secret_key=secret_key)
    assert email == user_sample.email


def test_get_email_from_expired_token(secret_key: str, token_info: dict[str, str | datetime]):
    expired_token_info: dict[str, Any] = {**token_info, 'exp': datetime.utcnow() - timedelta(minutes=1)}
    expired_token = jwt.encode(expired_token_info, secret_key)
    with pytest.raises(exceptions.Unauthorized):
        user_services.get_email_from_token(token=expired_token, secret_key=secret_key)


def test_get_email_from_token_without_sub(secret_key: str, token_info: dict[str, str | datetime]):
    token_info_without_sub = token_info.copy()
    token_info_without_sub.pop('sub')
    no_sub_token = jwt.encode(token_info_without_sub, secret_key)
    with pytest.raises(exceptions.Unauthorized):
        user_services.get_email_from_token(token=no_sub_token, secret_key=secret_key)


def test_get_email_from_token_with_empty_email(secret_key: str, token_info: dict[str, str | datetime]):
    token_info_with_empty_mail: dict[str, Any] = {**token_info, 'sub': ''}
    empty_mail_token = jwt.encode(token_info_with_empty_mail, secret_key)
    with pytest.raises(exceptions.Unauthorized):
        user_services.get_email_from_token(token=empty_mail_token, secret_key=secret_key)


def test_get_email_from_bad_signed_token(secret_key: str, token_info: dict[str, str | datetime]):
    other_secret_key = '91eaddafe18f273360800647aa08965f9cccbc1248d5748975a743d0f4b03ee6'  # noqa: S105
    bad_signature_token = jwt.encode(token_info, other_secret_key)
    with pytest.raises(exceptions.Unauthorized):
        user_services.get_email_from_token(token=bad_signature_token, secret_key=secret_key)
