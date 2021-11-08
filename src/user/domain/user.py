from dataclasses import asdict
from dataclasses import dataclass
from typing import TYPE_CHECKING

from src.user.domain.user_exceptions import UserAlreadyRegistered

if TYPE_CHECKING:
    from src.user.domain.user_repository import UserRepository


@dataclass
class User:
    name: str
    phone: str
    email: str
    verified: bool = False

    def to_dict(self) -> dict[str, str | bool]:
        return asdict(self)


def register_new_user(name: str, phone: str, email: str, user_repository: 'UserRepository') -> User:
    if user_repository.has(email):
        raise UserAlreadyRegistered
    new_user = User(name=name, phone=phone, email=email)
    user_repository.add(new_user)
    return new_user
