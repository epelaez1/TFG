from abc import ABC
from abc import abstractmethod

from bson import ObjectId

from src.venue.domain.exceptions import VenueDoesNotExist
from src.venue.domain.venue import Venue


class VenueRepository(ABC):

    @abstractmethod
    def has(self, id_: ObjectId | str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def add(self, venue: Venue) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, id_: ObjectId | str) -> Venue:
        raise NotImplementedError


class BasicVenueRepository(VenueRepository):

    def __init__(self) -> None:
        self.venues: dict[str, Venue] = {}

    def add(self, venue: Venue) -> None:
        self.venues[str(venue.id)] = venue

    def has(self, id_: str | ObjectId) -> bool:
        return str(id_) in self.venues

    def get(self, id_: str | ObjectId) -> Venue:
        venue = self.venues.get(str(id))
        if venue is None:
            raise VenueDoesNotExist
        return venue
