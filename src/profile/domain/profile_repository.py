from abc import ABC
from abc import abstractmethod

from src.profile.domain.exceptions import ProfileDoesNotExist
from src.profile.domain.profile import Profile


class ProfileRepository(ABC):

    @abstractmethod
    def has(self, email: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def add(self, profile: Profile) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, email: str) -> Profile:
        raise NotImplementedError


class BasicProfileRepository(ProfileRepository):

    def __init__(self) -> None:
        self.profiles: dict[str, Profile] = {}

    def add(self, profile: Profile) -> None:
        self.profiles[profile.email] = profile

    def has(self, email: str) -> bool:
        return email in self.profiles

    def get(self, email: str) -> Profile:
        if not self.has(email):
            raise ProfileDoesNotExist()
        return self.profiles[email]
