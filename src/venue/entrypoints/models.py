from datetime import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel
from pydantic import Field

from src.resources.pydantic_types.object_id import PyObjectId


class Point(BaseModel):
    type: str = 'Point'
    coordinates: list[float]


class NewVenue(BaseModel):
    name: str
    description: str
    province: str
    country: str
    geolocation: Point


class PrivateSpot(BaseModel):
    spot_number: int
    price: int
    name: Optional[str]
    description: Optional[str]


class PublicVenue(BaseModel):
    id: PyObjectId = Field(alias='_id')
    name: str
    description: str
    province: str
    country: str
    geolocation: Point
    private_spots: dict[int, PrivateSpot]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
        }


class Venue(PublicVenue):
    owner_email: str


class PublicEmployeeList(BaseModel):
    employee_name: str
    code: str


class EmployeeList(PublicEmployeeList):
    users: list[str]


class PublicSpotOffer(BaseModel):
    spot_number: int
    price: int
    available: bool


class PrivateSpotOffer(PublicSpotOffer):
    buyer_email: Optional[str]
    users_list: list[str]


class BaseSocialEvent(BaseModel):
    id: PyObjectId = Field(alias='_id')
    venue_id: str
    name: str
    description: str
    start_date: datetime
    end_date: datetime

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
        }


class PublicSocialEvent(BaseSocialEvent):
    private_spot_offers: list[PublicSpotOffer]
    employee_lists: dict[str, PublicEmployeeList]


class SocialEvent(BaseSocialEvent):
    owner_email: str
    private_spot_offers: list[PrivateSpotOffer]
    employee_lists: dict[str, EmployeeList]
    people_inside: list[str]
    people_history: list[str]


class NewSocialEvent(BaseModel):
    name: str
    description: str
    start_date: datetime
    end_date: datetime
