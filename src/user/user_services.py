from src.user.domain.user import register_new_user
from src.user.domain.user import User
from src.user.domain.user_repository import UserRepository


def register_user(name: str, email: str, phone: str, user_repository: UserRepository) -> User:
    return register_new_user(name=name, email=email, phone=phone, user_repository=user_repository)
