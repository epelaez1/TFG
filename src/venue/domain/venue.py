from bson import ObjectId
from geojson_pydantic import Point
from pydantic import BaseModel
from pydantic import Field

from src.resources.pydantic_types.object_id import PyObjectId


class Venue(BaseModel):
    id: PyObjectId = Field(alias='_id', default_factory=ObjectId)
    name: str
    description: str
    province: str
    country: str
    geolocation: Point
    owner_email: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
        }
