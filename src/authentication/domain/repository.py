from abc import ABC
from abc import abstractmethod

from src.authentication.domain import exceptions
from src.authentication.domain.entities.credentials import Credentials


class CredentialsRepository(ABC):

    @abstractmethod
    def has(self, email: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def add(self, credentials: Credentials) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, email: str) -> Credentials:
        raise NotImplementedError

    @abstractmethod
    def update(self, email: str, new_credentials: Credentials) -> None:
        raise NotImplementedError


class BasicCredentialsRepository(CredentialsRepository):

    def __init__(self) -> None:
        self.credentials_store: dict[str, Credentials] = {}

    def add(self, credentials: Credentials) -> None:
        self.credentials_store[credentials.email] = credentials

    def has(self, email: str) -> bool:
        return email in self.credentials_store

    def get(self, email: str) -> Credentials:
        if not self.has(email):
            raise exceptions.UserDoesNotExist()
        return self.credentials_store[email]

    def update(self, email: str, new_credentials: Credentials) -> None:
        self.credentials_store[email] = new_credentials
