from datetime import datetime
from typing import Any
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel
from pydantic import Field

from src.resources.pydantic_types.object_id import PyObjectId


class EmployeeList(BaseModel):
    employee_name: str
    code: str

    def __hash__(self) -> int:
        return hash(self.code)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, EmployeeList):
            return False
        return self.code == other.code


class PrivateSpotOffer(BaseModel):
    spot_number: int
    available: bool = True
    price: int
    buyer_email: Optional[str] = None
    users_list: list[str] = Field(default_factory=list)

    def __hash__(self) -> int:
        return hash(self.spot_number)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, PrivateSpotOffer):
            return False
        return self.spot_number == other.spot_number


class SocialEvent(BaseModel):
    id: PyObjectId = Field(alias='_id', default_factory=ObjectId)
    owner_email: str
    venue_id: str
    name: str
    description: str
    start_date: datetime
    end_date: datetime
    private_spot_offers: set[PrivateSpotOffer]
    employee_lists: set[EmployeeList] = Field(default_factory=set)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
        }
