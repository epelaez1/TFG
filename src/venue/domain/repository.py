from abc import ABC
from abc import abstractmethod

from src.venue.domain.entities.social_event import SocialEvent
from src.venue.domain.entities.venue import Venue
from src.venue.domain.exceptions import SocialEventDoesNotExist
from src.venue.domain.exceptions import VenueDoesNotExist


class VenueRepository(ABC):  # noqa: WPS214  Too many methods

    @abstractmethod
    def has_venue(self, venue_id: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def add_venue(self, venue: Venue) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_venue(self, venue_id: str) -> Venue:
        raise NotImplementedError

    @abstractmethod
    def update_venue(self, venue_id: str, new_venue: Venue) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_social_event(self, social_event_id: str) -> SocialEvent:
        raise NotImplementedError

    @abstractmethod
    def has_social_event(self, social_event_id: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def add_social_event(self, social_event: SocialEvent) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_all_venues(self) -> list[Venue]:
        raise NotImplementedError

    @abstractmethod
    def get_all_social_events(self) -> list[SocialEvent]:
        raise NotImplementedError

    @abstractmethod
    def get_social_events_of_venue(self, venue_id: str) -> list[SocialEvent]:
        raise NotImplementedError

    @abstractmethod
    def update_social_event(self, social_event_id: str, new_social_event: SocialEvent) -> None:
        raise NotImplementedError


class BasicVenueRepository(VenueRepository):  # noqa: WPS214  Too many methods

    def __init__(self) -> None:
        self.venues: dict[str, Venue] = {}
        self.social_events: dict[str, SocialEvent] = {}

    def add_venue(self, venue: Venue) -> None:
        self.venues[str(venue.id)] = venue

    def has_venue(self, venue_id: str) -> bool:
        return venue_id in self.venues

    def get_venue(self, venue_id: str) -> Venue:
        venue = self.venues.get(venue_id)
        if venue is None:
            raise VenueDoesNotExist()
        return venue

    def update_venue(self, venue_id: str, new_venue: Venue) -> None:
        self.venues[venue_id] = new_venue

    def has_social_event(self, social_event_id: str) -> bool:
        return social_event_id in self.social_events

    def get_social_event(self, social_event_id: str) -> SocialEvent:
        if not self.has_social_event(social_event_id):
            raise SocialEventDoesNotExist()
        return self.social_events[social_event_id]

    def add_social_event(self, social_event: SocialEvent) -> None:
        self.social_events[str(social_event.id)] = social_event

    def get_all_venues(self) -> list[Venue]:
        return list(self.venues.values())

    def get_all_social_events(self) -> list[SocialEvent]:
        return list(self.social_events.values())

    def get_social_events_of_venue(self, venue_id: str) -> list[SocialEvent]:
        return [social_event for social_event in self.social_events.values() if social_event.venue_id == venue_id]

    def update_social_event(self, social_event_id: str, new_social_event: SocialEvent) -> None:
        self.social_events[social_event_id] = new_social_event
