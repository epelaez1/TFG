from datetime import datetime
from typing import Optional

from geojson_pydantic import Point
from pydantic import BaseModel

from src.resources.pydantic_types.object_id import PyObjectId


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
    id: PyObjectId
    name: str
    description: str
    province: str
    country: str
    geolocation: Point
    private_spots: set[PrivateSpot]


class Venue(PublicVenue):
    owner_email: str


class PublicEmployeeList(BaseModel):
    employee_name: str
    code: str


class EmployeeList(PublicEmployeeList):
    users: set[str]


class PublicSpotOffer(BaseModel):
    spot_number: int
    price: int
    available: bool


class PrivateSpotOffer(PublicSpotOffer):
    buyer_email: Optional[str]
    users_list: list[str]


class BaseSocialEvent(BaseModel):
    id: PyObjectId
    venue_id: str
    name: str
    description: str
    start_date: datetime
    end_date: datetime


class PublicSocialEvent(BaseSocialEvent):
    private_spot_offers: set[PublicSpotOffer]
    employee_lists: dict[str, PublicEmployeeList]


class SocialEvent(BaseModel):
    owner_email: str
    private_spot_offers: set[PrivateSpotOffer]
    employee_lists: dict[str, EmployeeList]
    people_inside: set[str]
    people_history: set[str]
