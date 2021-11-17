from datetime import timedelta
from typing import TYPE_CHECKING

from pydantic import BaseModel

from src.user.domain.exceptions import UserAlreadyRegistered
from src.user.domain.hashed_password import hash_password
from src.user.domain.hashed_password import HashedPassword
from src.user.domain.session import create_session_token
from src.user.domain.session import SessionToken
from src.user.domain.session import Unauthorized

if TYPE_CHECKING:
    from src.user.domain.user_repository import UserRepository


class User(BaseModel):
    name: str
    phone: str
    email: str
    hashed_password: HashedPassword
    verified: bool = False

    def verify_user(self, plain_password: str) -> bool:
        return self.hashed_password.verify_password(plain_password=plain_password)

    def get_session_token(self, secret_key: str) -> SessionToken:
        token_info = {'sub': self.email}
        token_duration = timedelta(minutes=60 * 24 * 3)
        return create_session_token(token_info, duration=token_duration, secret_key=secret_key)

    @classmethod
    def get_user_email_from_session_token(cls, secret_key: str, token: str) -> str:
        session_token = SessionToken(access_token=token)
        payload: dict[str, str] = session_token.decode_payload(secret_key=secret_key)
        email: str | None = payload.get('sub')
        if email is None or email == '':
            raise Unauthorized
        return email


def register_new_user(name: str, phone: str, email: str, password: str, user_repository: 'UserRepository') -> User:
    hashed_password: HashedPassword = hash_password(password)
    if user_repository.has(email):
        raise UserAlreadyRegistered
    new_user = User(name=name, phone=phone, email=email, hashed_password=hashed_password)
    user_repository.add(new_user)
    return new_user
