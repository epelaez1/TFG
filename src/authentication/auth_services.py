from src.authentication.domain import exceptions
from src.authentication.domain.credentials import Credentials
from src.authentication.domain.credentials import register
from src.authentication.domain.credentials import TokenData
from src.authentication.domain.credentials_repository import CredentialsRepository
from src.authentication.domain.session import SessionToken


def register_user(
    email: str,
    password: str,
    credentials_repository: CredentialsRepository,
    secret_key: str,
) -> SessionToken:
    new_credentials = register(email=email, password=password, credentials_repository=credentials_repository)
    return new_credentials.get_session_token(secret_key=secret_key)


def login(email: str, password: str, credentials_repository: CredentialsRepository, secret_key: str) -> SessionToken:
    cred: Credentials
    try:
        cred = credentials_repository.get(email=email)
    except exceptions.UserDoesNotExist as error:
        raise exceptions.IncorrectUsername() from error
    if not cred.verify_user(plain_password=password):
        raise exceptions.IncorrectPassword()
    return cred.get_session_token(secret_key=secret_key)


def get_session_token_data(token: str, secret_key: str) -> TokenData:
    return Credentials.get_session_token_data(secret_key=secret_key, token=token)


def authorize(token: str, secret_key: str) -> TokenData:
    token_data: TokenData = Credentials.get_session_token_data(secret_key=secret_key, token=token)
    if not token_data.has_profile:
        raise exceptions.UserWithoutProfile()
    return token_data


def authorize_profile_creation(token: str, secret_key: str) -> TokenData:
    return Credentials.get_session_token_data(secret_key=secret_key, token=token)


def update_profile(email: str, credentials_repository: CredentialsRepository, secret_key: str) -> SessionToken:
    credentials = credentials_repository.get(email=email)
    credentials.has_profile = True
    credentials_repository.update(email=email, new_credentials=credentials)
    return credentials.get_session_token(secret_key=secret_key)
