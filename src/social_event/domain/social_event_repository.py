from abc import ABC
from abc import abstractmethod

from src.social_event.domain.exceptions import SocialEventDoesNotExist
from src.social_event.domain.social_event import SocialEvent


class SocialEventRepository(ABC):

    @abstractmethod
    def get(self, social_event_id: str) -> SocialEvent:
        raise NotImplementedError()

    @abstractmethod
    def has(self, social_event_id: str) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def add(self, social_event: SocialEvent) -> None:
        raise NotImplementedError()


class BasicSocialEventRepository(SocialEventRepository):

    def __init__(self) -> None:
        self.social_events: dict[str, SocialEvent] = {}

    def has(self, social_event_id: str) -> bool:
        return social_event_id in self.social_events

    def get(self, social_event_id: str) -> SocialEvent:
        if not self.has(social_event_id):
            raise SocialEventDoesNotExist()
        return self.social_events[social_event_id]

    def add(self, social_event: SocialEvent) -> None:
        self.social_events[str(social_event.id)] = social_event
