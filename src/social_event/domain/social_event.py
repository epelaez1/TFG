from datetime import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel
from pydantic import Field

from src.resources.pydantic_types.object_id import PyObjectId


class EmployeesList(BaseModel):
    employee_name: str
    code: str
    subscribed_user: list[str] = Field(default_factory=list)


class PrivateSpot(BaseModel):
    spot_id: str
    spot_number: int
    available: bool = True
    price: int
    owner: Optional[str] = None
    users_list: list[str] = Field(default_factory=list)


class SocialEvent(BaseModel):
    id: PyObjectId = Field(alias='_id', default_factory=ObjectId)
    venue_id: str
    name: str
    description: str
    start_date: datetime
    end_date: datetime
    employee_lists: dict[str, EmployeesList] = Field(default_factory=dict)
    private_spots: list[PrivateSpot] = Field(default_factory=list)
