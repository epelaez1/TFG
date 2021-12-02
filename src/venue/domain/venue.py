from typing import Optional

from bson import ObjectId
from geojson_pydantic import Point
from pydantic import BaseModel
from pydantic import Field

from src.resources.pydantic_types.object_id import PyObjectId


class PrivateSpot(BaseModel):
    id: PyObjectId = Field(alias='_id', default_factory=ObjectId)
    spot_number: int
    price: int  # Maybe do unique
    name: Optional[str]
    description: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
        }


class Venue(BaseModel):
    id: PyObjectId = Field(alias='_id', default_factory=ObjectId)
    name: str
    description: str
    province: str
    country: str
    geolocation: Point
    owner_email: str
    private_spots: list[PrivateSpot] = Field(default_factory=list)
    private_spot_numbers: set[int] = Field(default_factory=set)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
        }
