from src.user.domain import exceptions
from src.user.domain.session import SessionToken
from src.user.domain.user import register_new_user
from src.user.domain.user import User
from src.user.domain.user_repository import UserRepository


def register_user(name: str, email: str, phone: str, password: str, user_repository: UserRepository) -> User:
    return register_new_user(name=name, email=email, phone=phone, password=password, user_repository=user_repository)


def login(email: str, password: str, user_repository: UserRepository, secret_key: str) -> SessionToken:
    if not user_repository.has(email=email):
        raise exceptions.IncorrectUsername()
    user: User = user_repository.get(email=email)
    if not user.verify_user(plain_password=password):
        raise exceptions.IncorrectPassword()
    return user.get_session_token(secret_key=secret_key)


def get_email_from_token(token: str, secret_key: str) -> str:
    return User.get_user_email_from_session_token(secret_key=secret_key, token=token)


def get_user(email: str, user_repository: UserRepository) -> User:
    return user_repository.get(email=email)
