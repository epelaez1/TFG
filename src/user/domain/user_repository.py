from abc import ABC
from abc import abstractmethod

from src.user.domain.exceptions import UserDoesNotExists
from src.user.domain.user import User


class UserRepository(ABC):

    @abstractmethod
    def has(self, email: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def add(self, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, email: str) -> User:
        raise NotImplementedError


class BasicUserRepository(UserRepository):

    def __init__(self) -> None:
        self.users: dict[str, User] = {}

    def add(self, user: User) -> None:
        self.users[user.email] = user

    def has(self, email: str) -> bool:
        return email in self.users

    def get(self, email: str) -> User:
        if not self.has(email):
            raise UserDoesNotExists
        return self.users[email]
