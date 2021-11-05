from abc import ABC, abstractmethod

from src.user.domain.user import User
from src.user.domain.user_exceptions import UserAlreadyRegistered


class UserRepository(ABC):

    @abstractmethod
    def has(self, email: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def add(self, user: User) -> None:
        raise NotImplementedError


class BasicUserRepository(UserRepository):

    def __init__(self) -> None:
        self.users: dict[str, User] = {}

    def add(self, user: User) -> None:
        if not self.has(user.email):
            self.users[user.email] = user
        else:
            raise UserAlreadyRegistered

    def has(self, email: str) -> bool:
        return email in self.users
