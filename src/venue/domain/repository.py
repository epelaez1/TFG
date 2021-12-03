from abc import ABC
from abc import abstractmethod

from src.venue.domain.entities.social_event import EmployeeList
from src.venue.domain.entities.social_event import SocialEvent
from src.venue.domain.entities.venue import PrivateSpot
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
    def add_private_spot(self, venue_id: str, private_spot: PrivateSpot) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_social_event(self, social_event_id: str) -> SocialEvent:
        raise NotImplementedError()

    @abstractmethod
    def has_social_event(self, social_event_id: str) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def add_social_event(self, social_event: SocialEvent) -> None:
        raise NotImplementedError()

    @abstractmethod
    def add_employee_list_to_social_event(self, social_event_id: str, employee_list: EmployeeList) -> None:
        raise NotImplementedError()


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

    def add_private_spot(self, venue_id: str, private_spot: PrivateSpot) -> None:
        self.venues[venue_id].private_spots.add(private_spot)

    def has_social_event(self, social_event_id: str) -> bool:
        return social_event_id in self.social_events

    def get_social_event(self, social_event_id: str) -> SocialEvent:
        if not self.has_social_event(social_event_id):
            raise SocialEventDoesNotExist()
        return self.social_events[social_event_id]

    def add_social_event(self, social_event: SocialEvent) -> None:
        self.social_events[str(social_event.id)] = social_event

    def add_employee_list_to_social_event(self, social_event_id: str, employee_list: EmployeeList) -> None:
        if social_event_id not in self.social_events:
            raise SocialEventDoesNotExist()
        social_event = self.social_events[social_event_id]
        social_event.employee_lists.add(employee_list)
