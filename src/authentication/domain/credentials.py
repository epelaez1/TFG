from datetime import timedelta
from typing import Any
from typing import TYPE_CHECKING

from pydantic import BaseModel

from src.authentication.domain import exceptions
from src.authentication.domain.hashed_password import hash_password
from src.authentication.domain.hashed_password import HashedPassword
from src.authentication.domain.session import create_session_token
from src.authentication.domain.session import SessionToken

if TYPE_CHECKING:
    from src.authentication.domain.credentials_repository import CredentialsRepository


class TokenData(BaseModel):
    email: str
    has_profile: bool = False


class Credentials(TokenData):
    hashed_password: HashedPassword

    def verify_user(self, plain_password: str) -> bool:
        return self.hashed_password.verify_password(plain_password=plain_password)

    def get_session_token(self, secret_key: str) -> SessionToken:
        token_data = TokenData(**self.dict())
        token_payload = token_data.dict()
        token_duration = timedelta(minutes=60 * 24 * 3)
        return create_session_token(token_payload, duration=token_duration, secret_key=secret_key)

    @classmethod
    def get_session_token_data(cls, secret_key: str, token: str) -> TokenData:
        session_token = SessionToken(access_token=token)
        payload: dict[str, Any] = session_token.decode_payload(secret_key=secret_key)
        if not isinstance(payload, dict):
            raise exceptions.Unauthorized()
        email: str | None = payload.get('email')
        if email is None or email == '':
            raise exceptions.Unauthorized()
        return TokenData(**payload)


def register(
    email: str,
    password: str,
    credentials_repository: 'CredentialsRepository',
) -> Credentials:
    hashed_password: HashedPassword = hash_password(password)
    if credentials_repository.has(email):
        raise exceptions.UserAlreadyRegistered()
    new_credentials = Credentials(email=email, hashed_password=hashed_password)
    credentials_repository.add(new_credentials)
    return new_credentials
