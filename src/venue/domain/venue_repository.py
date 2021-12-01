from abc import ABC
from abc import abstractmethod

from src.venue.domain.exceptions import VenueDoesNotExist
from src.venue.domain.venue import PrivateSpot
from src.venue.domain.venue import Venue


class VenueRepository(ABC):

    @abstractmethod
    def has(self, id_: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def add(self, venue: Venue) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, id_: str) -> Venue:
        raise NotImplementedError

    @abstractmethod
    def get_private_spot_numbers(self, id_: str) -> set[int]:
        raise NotImplementedError

    @abstractmethod
    def add_private_spot(self, id_: str, private_spot: PrivateSpot) -> None:
        raise NotImplementedError


class BasicVenueRepository(VenueRepository):

    def __init__(self) -> None:
        self.venues: dict[str, Venue] = {}

    def add(self, venue: Venue) -> None:
        self.venues[str(venue.id)] = venue

    def has(self, id_: str) -> bool:
        return id_ in self.venues

    def get(self, id_: str) -> Venue:
        venue = self.venues.get(id_)
        if venue is None:
            raise VenueDoesNotExist
        return venue

    def get_private_spot_numbers(self, id_: str) -> set[int]:
        if id_ not in self.venues:
            raise VenueDoesNotExist()
        return self.venues[id_].private_spot_numbers

    def add_private_spot(self, id_: str, private_spot: PrivateSpot) -> None:
        if id_ not in self.venues:
            raise VenueDoesNotExist()

        self.venues[id_].private_spot_numbers.add(private_spot.spot_number)
        self.venues[id_].private_spots.append(private_spot)
