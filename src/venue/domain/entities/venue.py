from typing import Any
from typing import Optional

from bson import ObjectId
from geojson_pydantic import Point
from pydantic import BaseModel
from pydantic import Field

from src.resources.pydantic_types.object_id import PyObjectId
from src.venue.domain import exceptions
from src.venue.domain.entities.social_event import SocialEvent


class PrivateSpot(BaseModel):
    spot_number: int
    price: int
    name: Optional[str]
    description: Optional[str]

    def __hash__(self) -> int:
        return hash(self.spot_number)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, PrivateSpot):
            return False
        return self.spot_number == other.spot_number

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
    private_spots: dict[int, PrivateSpot] = Field(default_factory=dict)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
        }

    @property
    def id_str(self) -> str:
        return str(self.id)

    def add_private_spot_offer_to_social_event(self, social_event: SocialEvent, spot_number: int) -> None:
        private_spot = self.private_spots.get(spot_number, None)
        if private_spot is None:
            raise exceptions.PrivateSpotNotFound()

        social_event.add_private_spot_offer(spot_number=private_spot.spot_number, price=private_spot.price)

    def add_private_spot(self, spot_number: int, name: str | None, description: str | None, price: int) -> None:
        if spot_number in self.private_spots:
            raise exceptions.PrivateSpotNumberAlreadyAssigned()

        private_spot = PrivateSpot(
            spot_number=spot_number,
            name=name,
            description=description,
            price=price,
        )

        self.private_spots[private_spot.spot_number] = private_spot

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Venue):
            return False
        return self.id == other.id
