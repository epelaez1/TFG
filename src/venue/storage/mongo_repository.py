from typing import Any

from bson import ObjectId
from pymongo.collection import Collection

from src.mongo_client import MongoDBClient
from src.venue.domain.entities.social_event import SocialEvent
from src.venue.domain.entities.venue import Venue
from src.venue.domain.exceptions import SocialEventDoesNotExist
from src.venue.domain.exceptions import VenueDoesNotExist
from src.venue.domain.repository import VenueRepository


VENUE_COLLECTION = 'venues'
SOCIAL_EVENT_COLLECTION = 'social_events'
ID = '_id'


class VenueMongoDB(VenueRepository):

    def __init__(self, client: MongoDBClient) -> None:
        self._client = client
        self.venue_collection: Collection = self._client.get_collection(VENUE_COLLECTION)
        self.social_event_collection: Collection = self._client.get_collection(SOCIAL_EVENT_COLLECTION)

    def has_venue(self, venue_id: str) -> bool:
        return int(self.venue_collection.count_documents({ID: ObjectId(venue_id)})) == 1

    def add_venue(self, venue: Venue) -> None:
        self.venue_collection.insert_one(venue.dict(by_alias=True))

    def get_venue(self, venue_id: str) -> Venue:
        venue_in_db: dict[str, Any] = self.venue_collection.find_one({ID: ObjectId(venue_id)})
        if venue_in_db is None:
            raise VenueDoesNotExist()
        return Venue(**venue_in_db)

    def get_social_event(self, social_event_id: str) -> SocialEvent:
        social_event_in_db: dict[str, Any] = self.social_event_collection.find_one({ID: ObjectId(social_event_id)})
        if social_event_in_db is None:
            raise SocialEventDoesNotExist()
        return SocialEvent(**social_event_in_db)

    def has_social_event(self, social_event_id: str) -> bool:
        return int(self.social_event_collection.count_documents({ID: ObjectId(social_event_id)})) == 1

    def add_social_event(self, social_event: SocialEvent) -> None:
        self.social_event_collection.insert_one(social_event.dict(by_alias=True))

    def get_all_venues(self) -> list[Venue]:
        return list(self.venue_collection.find())

    def get_all_social_events(self, page: int = 1) -> list[SocialEvent]:
        event_per_page = 40
        return list(self.social_event_collection.find().limit(event_per_page).skip(page - 1))

    def get_social_events_of_venue(self, venue_id: str) -> list[SocialEvent]:
        return list(self.social_event_collection.find({'venue_id': venue_id}))

    def update_social_event(self, social_event_id: str, new_social_event: SocialEvent) -> None:
        self.social_event_collection.update_one(
            {ID: ObjectId(social_event_id)},
            {'$set': new_social_event.dict(by_alias=True)},
        )

    def update_venue(self, venue_id: str, new_venue: Venue) -> None:
        self.venue_collection.update_one(
            {ID: ObjectId(venue_id)},
            {'$set': new_venue.dict(by_alias=True)},
        )

    def access_social_event(self, social_event_id: str, user_email: str) -> None:
        self.social_event_collection.update_one(
            {ID: ObjectId(social_event_id)},
            {'$addToSet': {'people_inside': user_email, 'people_history': user_email}},
        )

    def leave_social_event(self, social_event_id: str, user_email: str) -> None:
        self.social_event_collection.update_one(
            {ID: ObjectId(social_event_id)},
            {'$pull': {'people_inside': user_email}},
        )

    def join_social_event(self, social_event_id: str, employee_code: str, user_email: str) -> None:
        self.social_event_collection.update_one(
            {ID: ObjectId(social_event_id)},
            {'$addToSet': {f'employee_lists.{employee_code}.users': user_email}},
        )
