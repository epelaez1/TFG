from datetime import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel
from pydantic import Field

from src.resources.pydantic_types.object_id import PyObjectId


class EmployeeList(BaseModel):
    employee_name: str
    code: str

    def __hash__(self) -> int:
        return hash(self._key())

    def _key(self) -> str:
        return self.code


class PrivateSpot(BaseModel):
    spot_id: str
    spot_number: int
    available: bool = True
    price: int
    buyer_email: Optional[str] = None
    users_list: list[str] = Field(default_factory=list)


class SocialEvent(BaseModel):
    id: PyObjectId = Field(alias='_id', default_factory=ObjectId)
    owner_email: str
    venue_id: str
    name: str
    description: str
    start_date: datetime
    end_date: datetime
    employee_lists: set[EmployeeList] = Field(default_factory=set)
    private_spots: list[PrivateSpot] = Field(default_factory=list)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
        }
