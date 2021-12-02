from datetime import datetime
from datetime import timedelta

import pytest
from bson import ObjectId
from pydantic import BaseModel
from pydantic import Field

from src.resources.pydantic_types.object_id import PyObjectId
from src.social_event.domain.social_event_repository import BasicSocialEventRepository
from src.social_event.domain.social_event_repository import SocialEventRepository


def tomorrow() -> datetime:
    return datetime.utcnow() + timedelta(days=1)


def object_id_str() -> str:
    return str(ObjectId())


class SocialEventSample(BaseModel):
    venue_id: PyObjectId = Field(default_factory=object_id_str)
    name: str = 'Social Event'
    description: str = 'A great show'
    start_date: datetime = Field(default_factory=datetime.utcnow)
    end_date: datetime = Field(default_factory=tomorrow)


@pytest.fixture
def social_event_sample() -> SocialEventSample:
    return SocialEventSample()


@pytest.fixture
def social_event_repository() -> SocialEventRepository:
    return BasicSocialEventRepository()
