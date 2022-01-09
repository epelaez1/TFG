from datetime import datetime
from typing import Any
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel
from pydantic import Field

from src.resources.pydantic_types.object_id import PyObjectId
from src.venue.domain import exceptions


class EmployeeList(BaseModel):
    employee_name: str
    code: str
    users: set[str] = Field(default_factory=set)

    def join(self, author_email: str) -> None:
        self.users.add(author_email)

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
    private_spot_offers: set[PrivateSpotOffer]
    employee_lists: dict[str, EmployeeList] = Field(default_factory=dict)
    people_inside: set[str] = Field(default_factory=set)
    people_history: set[str] = Field(default_factory=set)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
        }

    def add_private_spot_offer(self, spot_number: int, price: int) -> None:
        new_spot_offer = PrivateSpotOffer(spot_number=spot_number, price=price)
        if new_spot_offer in self.private_spot_offers:
            raise exceptions.SpotOfferAlreadyExists()
        self.private_spot_offers.add(PrivateSpotOffer(spot_number=spot_number, price=price))

    def reserve_spot(self, author_email: str, spot_number: int) -> None:
        spot = next(
            (spot_offer for spot_offer in self.private_spot_offers if spot_offer.spot_number == spot_number),
            None,
        )
        if spot is None:
            raise exceptions.PrivateSpotOfferDoesNotExist()
        spot.reserve(author_email)

    def join(self, author_email: str, employee_code: str) -> None:
        self.employee_lists[employee_code].join(author_email)

    def add_employee_list(self, code: str, employee_name: str) -> None:
        if code in self.employee_lists:
            raise exceptions.EmployeeCodeAlreadyInUse()
        employee_list = EmployeeList(code=code, employee_name=employee_name)
        self.employee_lists[code] = employee_list

    def access_social_event(self, user_email: str) -> None:
        self.people_inside.add(user_email)
        self.people_history.add(user_email)

    def leave_social_event(self, user_email: str) -> None:
        if user_email not in self.people_inside:
            raise exceptions.UserIsNotInsideTheSocialEvent()
        self.people_inside.remove(user_email)
