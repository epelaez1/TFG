from datetime import datetime
from typing import Any
from typing import Optional
from typing import TYPE_CHECKING

from bson import ObjectId
from pydantic import BaseModel
from pydantic import Field

from src.resources.pydantic_types.object_id import PyObjectId
from src.venue.domain import exceptions

if TYPE_CHECKING:
    from src.venue.domain.repository import VenueRepository


class EmployeeList(BaseModel):
    employee_name: str
    code: str
    users: list[str] = Field(default_factory=list)

    def __hash__(self) -> int:
        return hash(self.code)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, EmployeeList):
            return False
        return self.code == other.code


class PrivateSpotOffer(BaseModel):
    spot_number: int
    price: int
    available: bool = True
    buyer_email: Optional[str] = None
    users_list: list[str] = Field(default_factory=list)

    def __hash__(self) -> int:
        return hash(self.spot_number)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, PrivateSpotOffer):
            return False
        return self.spot_number == other.spot_number

    def reserve(self, author_email: str) -> None:
        if not self.available:
            raise exceptions.PrivateSpotIsNotAvailable()
        self.available = False
        self.buyer_email = author_email
        self.users_list.append(author_email)


class SocialEvent(BaseModel):
    id: PyObjectId = Field(alias='_id', default_factory=ObjectId)
    owner_email: str
    venue_id: str
    name: str
    description: str
    start_date: datetime
    end_date: datetime
    private_spot_offers: list[PrivateSpotOffer]
    employee_lists: dict[str, EmployeeList] = Field(default_factory=dict)
    people_inside: list[str] = Field(default_factory=list)
    people_history: list[str] = Field(default_factory=list)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
        }

    @property
    def id_str(self) -> str:
        return str(self.id)

    def add_private_spot_offer(self, spot_number: int, price: int) -> None:
        new_spot_offer = PrivateSpotOffer(spot_number=spot_number, price=price)
        if new_spot_offer in self.private_spot_offers:
            raise exceptions.SpotOfferAlreadyExists()
        self.private_spot_offers.append(PrivateSpotOffer(spot_number=spot_number, price=price))

    def reserve_spot(self, author_email: str, spot_number: int) -> None:
        spot = next(
            (spot_offer for spot_offer in self.private_spot_offers if spot_offer.spot_number == spot_number),
            None,
        )
        if spot is None:
            raise exceptions.PrivateSpotOfferDoesNotExist()
        spot.reserve(author_email)

    def join(self, author_email: str, employee_code: str, venue_repository: 'VenueRepository') -> None:
        if employee_code not in self.employee_lists:
            raise exceptions.EmployeeCodeDoesNotExist()
        venue_repository.join_social_event(
            social_event_id=self.id_str,
            employee_code=employee_code,
            user_email=author_email,
        )

    def add_employee_list(self, code: str, employee_name: str) -> None:
        if code in self.employee_lists:
            raise exceptions.EmployeeCodeAlreadyInUse()
        employee_list = EmployeeList(code=code, employee_name=employee_name)
        self.employee_lists[code] = employee_list

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, SocialEvent):
            return False
        return self.id_str == other.id_str
